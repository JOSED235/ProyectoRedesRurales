"""Montaje del video final: video de Carol + audios de José con diapositivas."""
import json, os, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
# Uso: python edit.py [salida.mp4] [--preview]
# Necesita: pip install imageio-ffmpeg. Antes: python slides.py (genera diapositivas/).
ED = os.path.dirname(os.path.abspath(__file__))
VP = os.path.dirname(ED)                      # videopresentacion/
PNG = os.path.join(ED, "diapositivas")
WRK = os.path.join(ED, "work"); os.makedirs(WRK, exist_ok=True)
VID = os.path.join(VP, "VideoSustentacion.mp4")   # video de Carol (no versionado: pesa 122 MB)
AUD = os.path.join(VP, "audios")
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(VP, "VideoSustentacion_Final.mp4")
PREVIEW = "--preview" in sys.argv

VENC = ["-c:v", "libx264", "-preset", "veryfast" if PREVIEW else "slow", "-crf", "21", "-pix_fmt", "yuv420p", "-r", "30"]
AENC = ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]

def run(args):
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + args)
    if r.returncode: sys.exit("ffmpeg falló: " + " ".join(args[-3:]))

aud = json.load(open(os.path.join(ED, "transcripcion-audios.json")))  # marcas por palabra (faster-whisper)
def t(archivo, palabra, despues=0.0):
    """Inicio de la primera palabra que contiene `palabra` después de `despues`."""
    for s in aud[archivo]["segs"]:
        for a, b, w in s["w"]:
            if a >= despues and palabra.lower() in w.lower():
                return a
    raise KeyError((archivo, palabra, despues))

# ---------- 1. audio limpio y nivelado ----------
LIMPIEZA = "highpass=f=90,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=200,loudnorm=I=-16:TP=-1.5:LRA=7"
def limpiar(src, dst, extra=""):
    if not os.path.exists(dst):
        run(["-i", src, "-vn", "-af", (extra + "," if extra else "") + LIMPIEZA, "-ar", "48000", "-ac", "1", dst])
carol_wav = os.path.join(WRK, "carol.wav"); limpiar(VID, carol_wav)
jw = {}
for f in os.listdir(AUD):
    jw[f] = os.path.join(WRK, f.replace(".m4a", ".wav")); limpiar(os.path.join(AUD, f), jw[f])

# ---------- 2. segmentos con la voz de José ----------
def segmento_jose(nombre, archivo, cortes, diapositivas, cola=0.6, cabeza=0.25, fin_negro=0.0, ini_negro=0.0):
    """cortes: [(ini, fin), ...] en tiempo del audio original.
    diapositivas: [(png, t_inicio_original), ...] ordenadas."""
    # mapa de tiempo original -> tiempo en la salida
    def mapa(x):
        acc = cabeza
        for a, b in cortes:
            if x < a: return acc
            if x <= b: return acc + (x - a)
            acc += b - a
        return acc
    total = cabeza + sum(b - a for a, b in cortes) + cola
    # audio: recortes con fundidos cortos para que no se noten los cortes
    filt, ins = [], []
    for i, (a, b) in enumerate(cortes):
        filt.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.04:.3f}:d=0.04[c{i}]")
        ins.append(f"[c{i}]")
    filt.append("".join(ins) + f"concat=n={len(cortes)}:v=0:a=1,volume=-3dB,adelay={int(cabeza*1000)},apad=whole_dur={total:.3f}[a]")
    a_out = os.path.join(WRK, nombre + "_a.wav")
    run(["-i", jw[archivo], "-filter_complex", ";".join(filt), "-map", "[a]", "-ar", "48000", a_out])
    # video: lista de imágenes con duración
    lst = os.path.join(WRK, nombre + ".txt")
    tiempos = [0.0] + [mapa(x) for _, x in diapositivas[1:]] + [total]
    with open(lst, "w") as fh:
        for (png, _), t0, t1 in zip(diapositivas, tiempos, tiempos[1:]):
            fh.write(f"file '{os.path.join(PNG, png)}.png'\nduration {t1 - t0:.3f}\n")
        fh.write(f"file '{os.path.join(PNG, diapositivas[-1][0])}.png'\n")
    out = os.path.join(WRK, nombre + ".mp4")
    vf = "fps=30,format=yuv420p"
    if ini_negro: vf += f",fade=t=in:d={ini_negro}"
    if fin_negro: vf += f",fade=t=out:st={total-fin_negro:.3f}:d={fin_negro}"
    run(["-f", "concat", "-safe", "0", "-i", lst, "-i", a_out, "-vf", vf,
         *VENC, *AENC, "-t", f"{total:.3f}", "-shortest", out])
    return out

# ---------- 3. segmentos del video de Carol ----------
def segmento_carol(nombre, ini, fin, capas, fade_in=0.0, fade_out=0.0):
    """capas: [(png, t_ini_original, t_fin_original), ...] superpuestas con su transparencia."""
    dur = fin - ini
    args = ["-ss", f"{ini}", "-to", f"{fin}", "-i", VID, "-ss", f"{ini}", "-to", f"{fin}", "-i", carol_wav]
    for png, _, _ in capas:
        args += ["-loop", "1", "-t", f"{dur:.3f}", "-i", os.path.join(PNG, png + ".png")]
    f = ["[0:v]fps=30,scale=720:1280,setsar=1[v0]"]
    last = "v0"
    for i, (png, a, b) in enumerate(capas):
        a2, b2 = max(0, a - ini), min(dur, b - ini)
        f.append(f"[{last}][{i+2}:v]overlay=0:0:enable='between(t,{a2:.2f},{b2:.2f})'[v{i+1}]")
        last = f"v{i+1}"
    vf = f"[{last}]format=yuv420p"
    if fade_in: vf += f",fade=t=in:d={fade_in}"
    if fade_out: vf += f",fade=t=out:st={dur-fade_out:.3f}:d={fade_out}"
    f.append(vf + "[v]")
    af = f"[1:a]afade=t=in:d=0.06,afade=t=out:st={dur-0.08:.3f}:d=0.08"
    if fade_out: af = f"[1:a]afade=t=in:d=0.06,afade=t=out:st={dur-fade_out:.3f}:d={fade_out}"
    f.append(af + "[a]")
    out = os.path.join(WRK, nombre + ".mp4")
    run(args + ["-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]", *VENC, *AENC, out])
    return out

partes = []
# A1: presentación
A = "AudioA1.m4a"
partes.append(segmento_jose("j1", A, [(2.5, 29.2)],
    [("a1_portada", 0), ("a1_agenda", t(A, "Primero"))], cola=1.0, ini_negro=0.6))

# Carol, parte 1: demostración (sin la frase de «pacientes»)
partes.append(segmento_carol("c1", 0.0, 273.9, [
    ("e_demo", 0.3, 5.5),
    ("s_ping1", 111.0, 122.8), ("s_ping2", 123.1, 134.9), ("s_ping3", 135.3, 159.8),
    ("s_obst", 160.2, 185.0), ("s_offline", 185.6, 198.5),
    ("s_ssid", 199.0, 216.0), ("s_cert", 228.0, 245.5), ("s_portal", 247.0, 268.0)]))
partes.append(segmento_carol("c2", 286.6, 327.75, [
    ("s_guias", 287.0, 295.0), ("s_videos", 300.0, 321.0)]))

# A2 y A3: diseño
A = "Audio-A2.m4a"
partes.append(segmento_jose("j2a", A, [(2.3, 45.8)],
    [("a2_propuestas", 0), ("a2_consolidado", t(A, "compararlas") - 0.4)], cola=0.3))
A = "AudioA2-topologia.m4a"
partes.append(segmento_jose("j2b", A, [(3.0, 26.6)],
    [("a2_gns3", 0), ("a2_fisico", t(A, "Cuando") - 0.2)], cabeza=0.15, cola=0.3))
A = "AudioA3.m4a"
partes.append(segmento_jose("j3", A, [(3.55, 37.9)],
    [("a3_vlsm", 0), ("a3_relay", t(A, "DHCP", 25) - 0.4)], cabeza=0.15, cola=0.5))

# Carol, parte 2: explicación con diapositivas encima y comprobación por terminal
sl = [("o_topologia", 329.4, 343.3), ("o_vlans", 343.3, 381.6), ("o_troncal", 381.6, 393.2),
      ("o_matriz", 393.2, 404.0), ("o_cdn", 404.0, 424.8), ("o_nginx", 424.8, 446.8),
      ("o_squid", 446.8, 461.8), ("o_flujo", 461.8, 479.8), ("o_fallas", 479.8, 494.3)]
cap = [("e_terminal", 500.6, 505.5), ("s_serv", 507.0, 520.0), ("s_relay", 526.0, 538.0),
       ("s_ntp", 545.0, 564.0), ("s_fw", 565.0, 575.5)]
partes.append(segmento_carol("c3", 329.3, 575.5, sl + cap))

# A4: pruebas complementarias (sin la lectura del corchete ni el «por hardware» repetido)
A = "AudioA4.m4a"
partes.append(segmento_jose("j4", A, [(2.0, 41.85), (45.2, 62.40), (64.30, 71.6)],
    [("a4_p12", 0), ("a4_p13", t(A, "Cuando") - 0.3), ("a4_colas", t(A, "red", 28) - 0.6),
     ("a4_video", 45.2), ("a4_jellyfin", t(A, "No", 57) - 0.2)], cabeza=0.4, cola=0.4))

# A5: resultados y cierre
A = "AudioA5.m4a"
partes.append(segmento_jose("j5", A, [(2.3, 41.9)],
    [("a5_resultados", 0), ("a5_sinsenal", t(A, "importante") - 0.6), ("a5_futuro", t(A, "Para", 19) - 0.4),
     ("a5_cierre", t(A, "Todas", 33) - 0.3)], cabeza=0.3, cola=3.5, fin_negro=1.2))

# ---------- 4. unir ----------
lst = os.path.join(WRK, "partes.txt")
with open(lst, "w") as fh:
    for p in partes: fh.write(f"file '{p}'\n")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", OUT])
print("listo:", OUT)
