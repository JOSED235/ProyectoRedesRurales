"""Diapositivas verticales (720x1280) con la identidad visual del portal del hub."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ED = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ED))
IMG = os.path.join(REPO, "docs", "img")
OUT = os.path.join(ED, "diapositivas"); os.makedirs(OUT, exist_ok=True)
W, H = 720, 1280

C = dict(niebla="#EEF3EF", paramo="#173B2F", guadua="#2F7D4F", rio="#1D6A8A",
         buganvilla="#A8326A", maiz="#F2B632", cielo="#D7E8EC", sierra="#9CC3AE",
         sierra2="#5E9C7C", muted="#4F6259", line="#D3DED8", blanco="#FFFFFF",
         edu="#E2F0E6", salud="#DDEDF3", ocio="#F6E1EA", mark="#FBE3A6")

# Fuentes del portal convertidas de .woff2 a .ttf (configs/servidor/www/fuentes/) con fontTools
F = os.path.join(ED, "fuentes")
def bric(size, w=700):
    f = ImageFont.truetype(os.path.join(F, "bricolage-grotesque-latin-wght-normal.ttf"), size)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def atk(size, bold=False):
    n = "atkinson-hyperlegible-latin-700-normal.ttf" if bold else "atkinson-hyperlegible-latin-400-normal.ttf"
    return ImageFont.truetype(os.path.join(F, n), size)
MONO = "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"
def mono(size):
    try: return ImageFont.truetype(MONO, size)
    except Exception: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)

# ---------------- utilidades ----------------
def wrap(d, text, font, width):
    out = []
    for par in text.split("\n"):
        line = ""
        for w in par.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= width: line = t
            else:
                if line: out.append(line)
                line = w
        out.append(line)
    return out

def text(d, xy, s, font, fill, width=None, gap=1.25, anchor="la"):
    x, y = xy
    lines = wrap(d, s, font, width) if width else s.split("\n")
    lh = int(font.size * gap)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill, anchor=anchor)
        y += lh
    return y

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def sierra(im, y0, h, sun=True, dark=False):
    """Cabecera de cordilleras en capas, como la del portal."""
    d = ImageDraw.Draw(im)
    d.rectangle((0, y0, W, y0 + h), fill=C["cielo"])
    if sun:
        cx, cy, r = int(W * 0.74), y0 + int(h * 0.38), int(h * 0.17)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C["maiz"])
    capas = [(C["sierra"], 0.55, 0.20, 1.3), (C["sierra2"], 0.68, 0.16, 2.1), (C["guadua"], 0.80, 0.12, 0.9), (C["paramo"], 0.90, 0.08, 1.7)]
    for col, base, amp, fase in capas:
        pts = [(0, y0 + h)]
        for x in range(0, W + 1, 12):
            yy = base + amp * (0.55 * math.sin(x / W * 5.1 + fase) + 0.30 * math.sin(x / W * 11.7 + fase * 2) + 0.15 * math.sin(x / W * 23 + fase))
            pts.append((x, y0 + int(h * yy)))
        pts.append((W, y0 + h))
        d.polygon(pts, fill=col)

def lienzo():
    return Image.new("RGB", (W, H), C["niebla"])

def encabezado(im, kicker, titulo, color=None):
    """Franja superior con cordillera baja, etiqueta y título."""
    sierra(im, 0, 150, sun=False)
    d = ImageDraw.Draw(im)
    d.text((48, 196), kicker.upper(), font=atk(22, True), fill=color or C["guadua"])
    y = text(d, (48, 230), titulo, bric(50), C["paramo"], width=W - 96, gap=1.08)
    return y + 18

def pie(im, s="Hub rural · Infraestructura de Redes 2 · Icesi"):
    d = ImageDraw.Draw(im)
    d.line((48, H - 70, W - 48, H - 70), fill=C["line"], width=2)
    d.text((48, H - 52), s, font=atk(20), fill=C["muted"])

def foto(im, path, box, borde=True, radio=18, modo="fit"):
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    src = Image.open(path).convert("RGB")
    if modo == "fit":
        k = min(bw / src.width, bh / src.height)
    else:
        k = max(bw / src.width, bh / src.height)
    nw, nh = int(src.width * k), int(src.height * k)
    src = src.resize((nw, nh), Image.LANCZOS)
    if modo != "fit":
        l, t = (nw - bw) // 2, (nh - bh) // 2
        src = src.crop((l, t, l + bw, t + bh)); nw, nh = bw, bh
    ox, oy = x0 + (bw - nw) // 2, y0 + (bh - nh) // 2
    m = Image.new("L", (nw, nh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, nw - 1, nh - 1), radio, fill=255)
    sh = Image.new("RGBA", (nw + 30, nh + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((15, 18, nw + 15, nh + 18), radio, fill=(23, 59, 47, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    im.paste(sh, (ox - 15, oy - 15), sh)
    im.paste(src, (ox, oy), m)
    if borde:
        ImageDraw.Draw(im).rounded_rectangle((ox, oy, ox + nw - 1, oy + nh - 1), radio, outline=C["line"], width=2)
    return (ox, oy, ox + nw, oy + nh)

def tarjeta(d, box, titulo, cuerpo, acento, fondo=C["blanco"], tsize=30, bsize=25):
    rrect(d, box, 20, fill=fondo, outline=C["line"], width=2)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0, y0, x0 + 10, y1), 5, fill=acento)
    y = text(d, (x0 + 32, y0 + 22), titulo, bric(tsize), C["paramo"], width=x1 - x0 - 56, gap=1.1)
    if cuerpo:
        text(d, (x0 + 32, y + 6), cuerpo, atk(bsize), C["paramo"], width=x1 - x0 - 56, gap=1.3)

def vinetas(d, xy, items, width, size=28, color=None, gap=18, punto=None):
    x, y = xy; f = atk(size)
    for it in items:
        d.ellipse((x, y + size * 0.42, x + 12, y + size * 0.42 + 12), fill=punto or C["guadua"])
        y = text(d, (x + 30, y), it, f, color or C["paramo"], width=width - 30, gap=1.28) + gap
    return y

def caja(d, cx, cy, w, h, titulo, sub=None, fondo=C["blanco"], borde=C["paramo"], tcol=None, tsize=26, ssize=21):
    box = (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)
    rrect(d, box, 16, fill=fondo, outline=borde, width=3)
    if sub:
        d.text((cx, cy - 6), titulo, font=bric(tsize), fill=tcol or C["paramo"], anchor="ms")
        yy = cy + 22
        for ln in sub.split("\n"):
            d.text((cx, yy), ln, font=atk(ssize), fill=C["muted"], anchor="ms"); yy += int(ssize * 1.2)
    else:
        d.text((cx, cy), titulo, font=bric(tsize), fill=tcol or C["paramo"], anchor="mm")
    return box

def flecha(d, p0, p1, col=None, w=4, doble=False, etiqueta=None):
    col = col or C["paramo"]
    d.line((p0, p1), fill=col, width=w)
    def punta(a, b):
        ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = 16
        p = [b, (b[0] - L * math.cos(ang - 0.45), b[1] - L * math.sin(ang - 0.45)), (b[0] - L * math.cos(ang + 0.45), b[1] - L * math.sin(ang + 0.45))]
        d.polygon(p, fill=col)
    punta(p0, p1)
    if doble: punta(p1, p0)
    if etiqueta:
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        f = atk(20, True); tw = d.textlength(etiqueta, font=f)
        rrect(d, (mx - tw / 2 - 10, my - 16, mx + tw / 2 + 10, my + 16), 10, fill=C["niebla"])
        d.text((mx, my), etiqueta, font=f, fill=col, anchor="mm")

def guardar(im, nombre):
    im.save(os.path.join(OUT, nombre + ".png"))

# ---------------- diapositivas ----------------
def portada():
    im = lienzo(); sierra(im, 0, 560)
    d = ImageDraw.Draw(im)
    d.text((48, 610), "PROYECTO FINAL · INFRAESTRUCTURA DE REDES 2", font=atk(22, True), fill=C["guadua"])
    y = text(d, (48, 650), "Hub rural sin Internet", bric(68), C["paramo"], width=W - 96, gap=1.05)
    y = text(d, (48, y + 10), "Red local autónoma para una unidad móvil de atención comunitaria en zonas rurales", atk(30), C["paramo"], width=W - 96, gap=1.3)
    y += 40
    d.line((48, y, 200, y), fill=C["maiz"], width=6); y += 34
    y = text(d, (48, y), "José David Rodríguez Pinilla", bric(34, 600), C["paramo"])
    y = text(d, (48, y + 4), "Carol Andrea Mosquera", bric(34, 600), C["paramo"])
    y = text(d, (48, y + 26), "Profesor: Andrés Navarro Cadavid, Ph.D.", atk(25), C["muted"])
    text(d, (48, y + 4), "Universidad Icesi · Cali · noviembre de 2026", atk(25), C["muted"])
    guardar(im, "a1_portada")

def agenda():
    im = lienzo(); y = encabezado(im, "Contenido", "Lo que verá en este video")
    d = ImageDraw.Draw(im)
    items = [("1", "Demostración en el laboratorio", "Equipos, Starlink, portal y contenido sin conexión", C["guadua"]),
             ("2", "De dónde salió el diseño", "Dos propuestas, diseño consolidado y GNS3", C["rio"]),
             ("3", "Cómo funciona por dentro", "VLAN, direccionamiento, CDN, caché y seguridad", C["buganvilla"]),
             ("4", "Pruebas y resultados", "Lo que se midió y lo que falta para operar en campo", C["maiz"])]
    y += 30
    for n, t, s, col in items:
        d.ellipse((48, y, 118, y + 70), fill=col)
        d.text((83, y + 35), n, font=bric(38), fill=C["blanco"] if col != C["maiz"] else C["paramo"], anchor="mm")
        text(d, (145, y + 2), t, bric(32), C["paramo"], width=W - 200)
        text(d, (145, y + 46), s, atk(24), C["muted"], width=W - 200)
        y += 175
    pie(im); guardar(im, "a1_agenda")

def propuestas():
    im = lienzo(); y = encabezado(im, "Fase 1 · Plan", "Dos propuestas individuales")
    d = ImageDraw.Draw(im)
    tarjeta(d, (48, y + 10, W - 48, y + 380), "Versión de José",
            "Raspberry Pi 5 como único equipo: enrutador, DHCP/DNS, portal cautivo (openNDS) y caché Squid.\nBloque 10.10.0.0/16 y enlace LTE.\nAporte: caché en tres niveles, presupuesto del disco, cronograma y riesgos.", C["guadua"])
    tarjeta(d, (48, y + 410, W - 48, y + 780), "Versión de Carol",
            "Mini PC i5 como enrutador router-on-a-stick, router 4G y túnel WireGuard.\nBloque 10.20.0.0/22 con cuatro VLAN calculadas con VLSM.\nAporte: método VLSM, sumarización y matriz de tráfico entre VLAN.", C["rio"])
    pie(im); guardar(im, "a2_propuestas")

def consolidado():
    im = lienzo(); y = encabezado(im, "Fase 1 · Diseño consolidado", "Separar la red de los servicios")
    d = ImageDraw.Draw(im)
    tarjeta(d, (48, y + 10, W - 48, y + 230), "MikroTik RouterOS 7: la red",
            "VLAN 10/20/30, NAT, portal cautivo (Hotspot), firewall entre VLAN, colas de ancho de banda y relay DHCP.", C["paramo"], fondo=C["edu"])
    tarjeta(d, (48, y + 260, W - 48, y + 480), "Raspberry Pi 5 “hub”: los servicios",
            "DNS y DHCP, hora de red, portal web, Wikipedia sin conexión, caché Squid y CDN de video.", C["rio"], fondo=C["salud"])
    yy = y + 520
    rrect(d, (48, yy, W - 48, yy + 120), 18, fill=C["mark"])
    text(d, (78, yy + 24), "Si el servidor falla o se actualiza, la red sigue funcionando.", bric(29, 650), C["paramo"], width=W - 156)
    yy += 160
    text(d, (48, yy), "Se conserva de José: caché y almacenamiento.\nSe conserva de Carol: VLSM y matriz de tráfico.", atk(25), C["muted"], width=W - 96, gap=1.4)
    pie(im); guardar(im, "a2_consolidado")

def gns3():
    im = lienzo(); y = encabezado(im, "Fase 1.2 · Laboratorio virtual", "Primero en GNS3")
    d = ImageDraw.Draw(im)
    b = foto(im, f"{IMG}/f12-gns3-topologia.png", (48, y + 10, W - 48, y + 440))
    yy = b[3] + 40
    vinetas(d, (48, yy), ["MikroTik CHR 7.25: el mismo RouterOS del equipo físico",
                          "Ubuntu Server 24.04 como servidor del hub",
                          "Un cliente por VLAN y etiquetas 802.1Q verificadas en Wireshark"], W - 96, size=27)
    pie(im); guardar(im, "a2_gns3")

def fisico():
    im = lienzo(); y = encabezado(im, "Fase 2 · Prototipo", "Paso a lo físico, un equipo a la vez")
    d = ImageDraw.Draw(im)
    pasos = [("30/10", "Raspberry Pi 5 física"), ("05/11", "MikroTik CCR2004"), ("13/11", "Punto de acceso TP-Link"),
             ("19/11", "Starlink Mini"), ("20/11", "CDN de video")]
    x = 92; yy = y + 30
    d.line((x, yy + 20, x, yy + 20 + 80 * (len(pasos) - 1)), fill=C["sierra"], width=6)
    for f_, t in pasos:
        d.ellipse((x - 18, yy + 2, x + 18, yy + 38), fill=C["guadua"], outline=C["niebla"], width=4)
        d.text((x + 40, yy + 4), f_, font=atk(24, True), fill=C["guadua"])
        d.text((x + 140, yy + 2), t, font=bric(30, 600), fill=C["paramo"])
        yy += 80
    b = foto(im, f"{IMG}/f23-foto-montaje.png", (48, yy + 10, W - 48, yy + 270), modo="cover")
    rrect(d, (48, b[3] + 26, W - 48, b[3] + 106), 16, fill=C["mark"])
    d.text((76, b[3] + 66), "Después de cada cambio: respaldo /export", font=bric(27, 650), fill=C["paramo"], anchor="lm")
    pie(im); guardar(im, "a2_fisico")

def vlsm():
    im = lienzo(); y = encabezado(im, "Direccionamiento", "VLSM sobre 10.20.0.0/24")
    d = ImageDraw.Draw(im)
    # barra proporcional de 256 direcciones
    x0, x1, by = 48, W - 48, y + 30; L = x1 - x0
    seg = [(0, 128, C["buganvilla"], "/25"), (128, 160, C["rio"], "/27"), (160, 176, C["paramo"], "/28"), (176, 256, C["line"], "libre")]
    for a, b, col, lab in seg:
        xa, xb = x0 + L * a / 256, x0 + L * b / 256
        d.rectangle((xa, by, xb - 3, by + 70), fill=col)
        d.text(((xa + xb) / 2, by + 35), lab, font=atk(22, True), fill=C["blanco"] if col != C["line"] else C["muted"], anchor="mm")
    d.text((x0, by + 82), ".0", font=atk(20), fill=C["muted"]); d.text((x0 + L / 2, by + 82), ".128", font=atk(20), fill=C["muted"], anchor="ma")
    d.text((x1, by + 82), ".255", font=atk(20), fill=C["muted"], anchor="ra")
    yy = by + 150
    filas = [("VLAN 30 · Pública", "10.20.0.0/25", "126 direcciones · gw .1", C["buganvilla"], C["ocio"]),
             ("VLAN 20 · Salud", "10.20.0.128/27", "30 direcciones · gw .129", C["rio"], C["salud"]),
             ("VLAN 10 · Administración", "10.20.0.160/28", "14 direcciones · gw .161", C["paramo"], C["edu"])]
    for t, red, det, col, fondo in filas:
        rrect(d, (48, yy, W - 48, yy + 150), 18, fill=fondo)
        d.rounded_rectangle((48, yy, 58, yy + 150), 5, fill=col)
        d.text((80, yy + 22), t, font=bric(30), fill=C["paramo"])
        d.text((80, yy + 66), red, font=mono(34), fill=col)
        d.text((80, yy + 108), det, font=atk(24), fill=C["muted"])
        yy += 172
    text(d, (48, yy + 10), "Libres para crecer: 10.20.0.176/28 y 10.20.0.192/26", atk(25), C["muted"], width=W - 96)
    pie(im); guardar(im, "a3_vlsm")

def relay():
    im = lienzo(); y = encabezado(im, "Direccionamiento", "DHCP con relay")
    d = ImageDraw.Draw(im)
    cx = W // 2
    caja(d, 190, y + 90, 260, 110, "Celular", "Hub-Salud · VLAN 20", fondo=C["salud"], borde=C["rio"])
    caja(d, 530, y + 90, 260, 110, "Celular", "Hub-Publica · VLAN 30", fondo=C["ocio"], borde=C["buganvilla"])
    m = caja(d, cx, y + 360, 440, 130, "MikroTik", "relay-salud · relay-publica", fondo=C["blanco"])
    r = caja(d, cx, y + 640, 440, 130, "Raspberry Pi 5", "dnsmasq · 10.20.0.162 · VLAN 10", fondo=C["edu"], borde=C["guadua"])
    flecha(d, (190, y + 150), (cx - 90, m[1] - 6), C["rio"], etiqueta="DHCP")
    flecha(d, (530, y + 150), (cx + 90, m[1] - 6), C["buganvilla"], etiqueta="DHCP")
    flecha(d, (cx, m[3] + 4), (cx, r[1] - 6), C["guadua"], doble=True, etiqueta="reenvío")
    yy = y + 735
    vinetas(d, (48, yy), ["Un solo servidor DHCP para las tres VLAN",
                          "La Raspberry no necesita estar en cada VLAN",
                          "Cada red recibe su gateway, DNS y hora"], W - 96, size=25, gap=12)
    pie(im); guardar(im, "a3_relay")

def topologia(nombre="o_topologia"):
    im = lienzo(); y = encabezado(im, "Arquitectura", "Topología del hub")
    d = ImageDraw.Draw(im); cx = W // 2
    a = caja(d, cx, y + 50, 240, 70, "Internet", fondo=C["cielo"], borde=C["muted"])
    s = caja(d, cx, y + 170, 330, 96, "Starlink Mini", "WAN por DHCP · CGNAT", fondo=C["cielo"], borde=C["muted"])
    m = caja(d, cx, y + 340, 520, 150, "MikroTik RouterOS 7", "VLAN · NAT · Hotspot · firewall · colas\nether9 WAN · ether10 hub · ether11 troncal", fondo=C["blanco"], tsize=30)
    flecha(d, (cx, a[3]), (cx, s[1] - 4), C["muted"])
    flecha(d, (cx, s[3]), (cx, m[1] - 4), C["muted"])
    r = caja(d, 175, y + 590, 270, 120, "Raspberry Pi 5", "“hub” · 10.20.0.162\nservicios + disco", fondo=C["edu"], borde=C["guadua"])
    p = caja(d, 545, y + 590, 270, 120, "Punto de acceso", "TP-Link · 10.20.0.163\nun SSID por VLAN", fondo=C["blanco"])
    d.line((cx - 120, m[3], 175, r[1]), fill=C["guadua"], width=4)
    d.line((cx + 120, m[3], 545, p[1]), fill=C["paramo"], width=6)
    d.text((40, y + 470), "acceso VLAN 10", font=atk(20, True), fill=C["guadua"])
    d.text((550, y + 470), "troncal 802.1Q", font=atk(20, True), fill=C["paramo"])
    s1 = caja(d, 430, y + 800, 200, 96, "Hub-Salud", "VLAN 20 · WPA2", fondo=C["salud"], borde=C["rio"], tsize=24)
    s2 = caja(d, 640, y + 800, 150, 96, "Hub-Publica", "VLAN 30", fondo=C["ocio"], borde=C["buganvilla"], tsize=22)
    d.line((520, p[3], 430, s1[1]), fill=C["rio"], width=3); d.line((570, p[3], 640, s2[1]), fill=C["buganvilla"], width=3)
    caja(d, 175, y + 800, 270, 96, "Portátil admin", "por cable · VLAN 10", fondo=C["blanco"], borde=C["muted"], tsize=24)
    pie(im); guardar(im, nombre)

def vlans():
    im = lienzo(); y = encabezado(im, "Segmentación", "Tres VLAN, tres grupos")
    d = ImageDraw.Draw(im)
    datos = [("VLAN 10 · Administración", "Solo por cable. Desde aquí se gestionan el MikroTik, el servidor y el punto de acceso.", C["paramo"], C["edu"]),
             ("VLAN 20 · Salud", "Wi-Fi Hub-Salud (WPA2) con usuario y contraseña. Ancho de banda garantizado y prioridad más alta.", C["rio"], C["salud"]),
             ("VLAN 30 · Pública", "Wi-Fi Hub-Publica, abierta. Portal cautivo con un clic; contenido local sin iniciar sesión.", C["buganvilla"], C["ocio"])]
    yy = y + 10
    for t, b, col, fondo in datos:
        tarjeta(d, (48, yy, W - 48, yy + 250), t, b, col, fondo=fondo, tsize=32, bsize=26)
        yy += 280
    pie(im); guardar(im, "o_vlans")

def troncal():
    im = lienzo(); y = encabezado(im, "Capa 2", "Etiquetas 802.1Q por SSID")
    d = ImageDraw.Draw(im); cx = W // 2
    c1 = caja(d, 180, y + 80, 250, 96, "Hub-Salud", "SSID de la VLAN 20", fondo=C["salud"], borde=C["rio"])
    c2 = caja(d, 540, y + 80, 250, 96, "Hub-Publica", "SSID de la VLAN 30", fondo=C["ocio"], borde=C["buganvilla"])
    p = caja(d, cx, y + 300, 380, 110, "Punto de acceso", "etiqueta cada trama", fondo=C["blanco"])
    flecha(d, (180, c1[3]), (cx - 80, p[1] - 4), C["rio"]); flecha(d, (540, c2[3]), (cx + 80, p[1] - 4), C["buganvilla"])
    m = caja(d, cx, y + 580, 440, 120, "MikroTik · ether11", "bridge con vlan-filtering", fondo=C["blanco"])
    d.line((cx, p[3], cx, m[1]), fill=C["paramo"], width=10)
    for i, (lab, col) in enumerate([("VLAN 10 sin etiqueta", C["paramo"]), ("VLAN 20 etiquetada", C["rio"]), ("VLAN 30 etiquetada", C["buganvilla"])]):
        d.text((cx + 30, p[3] + 24 + i * 40), lab, font=atk(23, True), fill=col)
    yy = m[3] + 50
    vinetas(d, (48, yy), ["Un solo cable lleva las tres redes",
                          "Todo el tráfico entre redes pasa por el MikroTik"], W - 96, size=27)
    pie(im); guardar(im, "o_troncal")

def matriz():
    im = lienzo(); y = encabezado(im, "Firewall", "Qué puede alcanzar cada red")
    d = ImageDraw.Draw(im)
    cols = ["Origen", "MikroTik", "Servidor", "Entre VLAN", "Internet"]
    filas = [("VLAN 10", "Gestión", "Todo", "Sí", "Sí"),
             ("VLAN 20", "DHCP, DNS, portal", "DNS, hora, web", "No", "Tras sesión"),
             ("VLAN 30", "DHCP, DNS, portal", "DNS, hora, web", "No", "Tras portal"),
             ("Internet", "No", "No", "—", "—")]
    xs = [48, 165, 318, 470, 592]; yy = y + 30
    rrect(d, (40, yy - 10, W - 40, yy + 60), 12, fill=C["paramo"])
    for x, c in zip(xs, cols): d.text((x + 6, yy + 25), c, font=atk(19, True), fill=C["blanco"], anchor="lm")
    yy += 80
    for fi in filas:
        for i, (x, v) in enumerate(zip(xs, fi)):
            col = C["paramo"]
            if v == "No": col = C["buganvilla"]
            if v in ("Sí", "Todo"): col = C["guadua"]
            text(d, (x + 6, yy), v, atk(22, i == 0 or v in ("No", "Sí")), col, width=(xs[i + 1] - x - 12) if i < 4 else W - 48 - x - 12, gap=1.15)
        yy += 110
        d.line((48, yy - 22, W - 48, yy - 22), fill=C["line"], width=2)
    rrect(d, (48, yy + 10, W - 48, yy + 150), 18, fill=C["mark"])
    text(d, (76, yy + 36), "La red pública no llega ni a salud ni a administración: 18 reglas en el MikroTik.", bric(27, 650), C["paramo"], width=W - 152)
    pie(im); guardar(im, "o_matriz")

def cdn():
    im = lienzo(); y = encabezado(im, "Contenido sin conexión", "El corazón: la CDN local")
    d = ImageDraw.Draw(im)
    b = foto(im, f"{IMG}/f23-portal-inicio.png", (48, y + 10, W - 48, y + 470))
    yy = b[3] + 34
    for i, (t, col, fondo) in enumerate([("Educación", C["guadua"], C["edu"]), ("Salud", C["rio"], C["salud"]), ("Ocio", C["buganvilla"], C["ocio"])]):
        x = 48 + i * 212
        rrect(d, (x, yy, x + 196, yy + 64), 32, fill=fondo, outline=col, width=3)
        d.text((x + 98, yy + 32), t, font=bric(26), fill=col, anchor="mm")
    vinetas(d, (48, yy + 100), ["Guías PDF propias y artículos de Wikipedia",
                                "Wikipedia en español sin conexión (Kiwix)",
                                "Videos educativos en el disco USB de /srv/cdn"], W - 96, size=26)
    pie(im); guardar(im, "o_cdn")

def nginx_dns():
    im = lienzo(); y = encabezado(im, "Servicios del hub", "HTTPS y nombres locales")
    d = ImageDraw.Draw(im)
    yy = y + 10
    for t, b, col in [("Nginx", "Sirve el portal, los PDF y los videos por HTTPS con un certificado *.hub.lan.", C["guadua"]),
                      ("dnsmasq", "Resuelve portal.hub.lan, wiki.hub.lan y cdn.hub.lan aunque no haya Internet.", C["rio"]),
                      ("Portal cautivo", "El servidor está en el walled garden: el contenido local se ve sin iniciar sesión.", C["buganvilla"])]:
        tarjeta(d, (48, yy, W - 48, yy + 175), t, b, col, tsize=30, bsize=25); yy += 195
    foto(im, f"{IMG}/f23-offline-starlink-sin-senal.png", (48, yy + 10, W - 48, yy + 230))
    pie(im); guardar(im, "o_nginx")

def squid():
    im = lienzo(); y = encabezado(im, "Caché", "Squid ahorra enlace satelital")
    d = ImageDraw.Draw(im); cx = W // 2
    c = caja(d, cx, y + 60, 300, 90, "Celular", "ya pasó el portal", fondo=C["ocio"], borde=C["buganvilla"])
    m = caja(d, cx, y + 250, 360, 100, "MikroTik", "regla pbr-squid", fondo=C["blanco"])
    s = caja(d, 175, y + 470, 270, 110, "Squid", "Raspberry · caché", fondo=C["edu"], borde=C["guadua"])
    st = caja(d, 545, y + 470, 270, 110, "Starlink", "salida directa", fondo=C["cielo"], borde=C["muted"])
    flecha(d, (cx, c[3]), (cx, m[1] - 4))
    flecha(d, (cx - 80, m[3]), (175, s[1] - 4), C["guadua"], etiqueta="HTTP")
    flecha(d, (cx + 80, m[3]), (545, st[1] - 4), C["rio"], etiqueta="HTTPS")
    yy = s[3] + 50
    vinetas(d, (48, yy), ["La segunda persona que pide lo mismo no gasta enlace",
                          "El tráfico cifrado no se descifra: protege los datos de salud",
                          "Reemplazo LFUDA: se queda lo más pedido"], W - 96, size=26)
    pie(im); guardar(im, "o_squid")

def flujo():
    im = lienzo(); y = encabezado(im, "Recorrido de un celular", "Del Wi-Fi a la página")
    d = ImageDraw.Draw(im)
    pasos = [("1", "Pide una dirección", "El MikroTik reenvía la solicitud al servidor, sin salir a Internet.", C["guadua"]),
             ("2", "Navega por HTTP", "La página pasa primero por la caché del servidor.", C["rio"]),
             ("3", "Navega por HTTPS", "Sale directo por la Starlink, sin interceptar.", C["buganvilla"]),
             ("4", "En todos los casos", "Se aplican las colas de ancho de banda de su grupo.", C["maiz"])]
    yy = y + 20
    for n, t, b, col in pasos:
        d.ellipse((48, yy, 108, yy + 60), fill=col)
        d.text((78, yy + 30), n, font=bric(32), fill=C["blanco"] if col != C["maiz"] else C["paramo"], anchor="mm")
        text(d, (135, yy + 4), t, bric(31), C["paramo"], width=W - 190)
        text(d, (135, yy + 50), b, atk(25), C["muted"], width=W - 190, gap=1.3)
        yy += 200
    pie(im); guardar(im, "o_flujo")

def fallas():
    im = lienzo(); y = encabezado(im, "Tolerancia a fallas", "Si algo falla, la red se protege sola")
    d = ImageDraw.Draw(im)
    tarjeta(d, (48, y + 10, W - 48, y + 300), "Si Squid se cae",
            "Netwatch lo detecta en unos 10 segundos y apaga el desvío. Se pierde la caché, no la navegación.", C["guadua"], fondo=C["edu"])
    tarjeta(d, (48, y + 330, W - 48, y + 660), "Si la Starlink no tiene señal",
            "El hub sigue entregando direcciones, nombres, hora, portal, documentos, Wikipedia y videos.", C["rio"], fondo=C["salud"])
    pie(im); guardar(im, "o_fallas")

def p12():
    im = lienzo(); y = encabezado(im, "Prueba P12", "La caché sí acelera")
    d = ImageDraw.Draw(im)
    d.text((48, y + 40), "0,57 s", font=bric(80), fill=C["muted"])
    flecha(d, (282, y + 92), (338, y + 92), C["guadua"], w=8)
    d.text((356, y + 40), "0,002 s", font=bric(80), fill=C["guadua"])
    text(d, (48, y + 160), "Primera descarga del archivo, y la segunda servida desde la caché de Squid.", atk(26), C["muted"], width=W - 96)
    b = foto(im, f"{IMG}/f23-p12-squid-hit.png", (48, y + 270, W - 48, y + 470))
    b2 = foto(im, f"{IMG}/f23-p12-celular-log.png", (48, b[3] + 40, W - 48, b[3] + 140))
    text(d, (48, b2[3] + 26), "En el celular: TCP_MEM_HIT, servido desde la memoria.", atk(25, True), C["paramo"], width=W - 96)
    pie(im); guardar(im, "a4_p12")

def p13():
    im = lienzo(); y = encabezado(im, "Prueba P13", "Squid apagado, la navegación sigue")
    d = ImageDraw.Draw(im)
    d.text((48, y + 20), "Squid detenido: la regla se desactiva", font=atk(25, True), fill=C["buganvilla"])
    b = foto(im, f"{IMG}/f23-p13-pbr-desactivado.png", (48, y + 60, W - 48, y + 360))
    d.text((48, b[3] + 30), "Squid encendido: se reactiva sola", font=atk(25, True), fill=C["guadua"])
    b2 = foto(im, f"{IMG}/f23-p13-pbr-reactivado.png", (48, b[3] + 70, W - 48, b[3] + 370))
    rrect(d, (48, b2[3] + 30, W - 48, b2[3] + 110), 16, fill=C["mark"])
    d.text((76, b2[3] + 70), "Detección en menos de 10 segundos", font=bric(28, 650), fill=C["paramo"], anchor="lm")
    pie(im); guardar(im, "a4_p13")

def colas():
    im = lienzo(); y = encabezado(im, "Prueba P15", "Ancho de banda por grupo")
    d = ImageDraw.Draw(im)
    tarjeta(d, (48, y + 10, 352, y + 250), "Pública", "2 Mbps de bajada por usuario\n20 Mbps el grupo", C["buganvilla"], fondo=C["ocio"], tsize=30, bsize=24)
    tarjeta(d, (368, y + 10, W - 48, y + 250), "Salud", "10 Mbps garantizados\nprioridad 1", C["rio"], fondo=C["salud"], tsize=30, bsize=24)
    b = foto(im, f"{IMG}/f23-hotspot-activo-prueba.png", (48, y + 290, W - 48, y + 760))
    text(d, (48, b[3] + 26), "Sesión del celular en el Hotspot y su cola dinámica dentro de la cola pública.", atk(24), C["muted"], width=W - 96)
    pie(im); guardar(im, "a4_colas")

def video():
    im = lienzo(); y = encabezado(im, "Fase 2.4 · CDN de video", "Video que arranca de inmediato")
    d = ImageDraw.Draw(im); cx = W // 2
    for i, (k, v) in enumerate([("Resolución", "720p"), ("Códec", "H.264 + AAC"), ("Tasa máxima", "1,2 Mbps"), ("Índice", "al inicio (faststart)")]):
        x = 48 + (i % 2) * 320; yy = y + 10 + (i // 2) * 130
        rrect(d, (x, yy, x + 304, yy + 112), 16, fill=C["blanco"], outline=C["line"], width=2)
        d.text((x + 22, yy + 20), k, font=atk(21), fill=C["muted"]); d.text((x + 22, yy + 52), v, font=bric(31), fill=C["paramo"])
    yy = y + 300
    c = caja(d, 175, yy + 70, 270, 100, "Celular", "adelanta el video", fondo=C["ocio"], borde=C["buganvilla"])
    n = caja(d, 545, yy + 70, 270, 100, "Nginx", "/srv/cdn/video", fondo=C["edu"], borde=C["guadua"])
    flecha(d, (c[2] + 4, yy + 50), (n[0] - 6, yy + 50), C["paramo"])
    flecha(d, (n[0] - 4, yy + 92), (c[2] + 6, yy + 92), C["guadua"])
    d.text((cx, yy + 160), "Range: bytes=…", font=mono(28), fill=C["paramo"], anchor="ma")
    d.text((cx, yy + 200), "206 Partial Content", font=mono(28), fill=C["guadua"], anchor="ma")
    vinetas(d, (48, yy + 280), ["Solo se envía el fragmento pedido",
                                "Cabe en los 2 Mbps de cada usuario",
                                "Se puede pausar y adelantar sin esperar"], W - 96, size=26)
    pie(im); guardar(im, "a4_video")

def jellyfin():
    im = lienzo(); y = encabezado(im, "Decisión de diseño", "¿Por qué no Jellyfin?")
    d = ImageDraw.Draw(im)
    tarjeta(d, (48, y + 10, W - 48, y + 270), "La Raspberry Pi 5 no tiene codificador de video por hardware",
            "Transcodificar en vivo para varios celulares saturaría la CPU y frenaría el DNS, el DHCP y la caché.", C["buganvilla"], fondo=C["ocio"], tsize=29)
    tarjeta(d, (48, y + 300, W - 48, y + 560), "Se codifica una sola vez",
            "El video se prepara antes con ffmpeg y el hub lo sirve como un archivo normal: solo lee del disco.", C["guadua"], fondo=C["edu"], tsize=29)
    d.text((48, y + 610), "ffmpeg · 720p · -maxrate 1200k · +faststart", font=mono(25), fill=C["muted"])
    pie(im); guardar(im, "a4_jellyfin")

def resultados():
    im = lienzo(); y = encabezado(im, "Resultados", "Pruebas en hardware físico")
    d = ImageDraw.Draw(im)
    for i, (n, t, col, fondo) in enumerate([("15/15", "pruebas de red y servicios", C["guadua"], C["edu"]), ("4/4", "pruebas de video", C["rio"], C["salud"])]):
        yy = y + 10 + i * 270
        rrect(d, (48, yy, W - 48, yy + 240), 22, fill=fondo)
        d.text((80, yy + 30), n, font=bric(120), fill=col)
        d.text((80, yy + 175), t, font=atk(30, True), fill=C["paramo"])
    yy = y + 570
    text(d, (48, yy), "DHCP por relay · DNS local · hora · portal cautivo por VLAN · HTTPS · contenido sin sesión · operación sin Internet · caché · conmutación de Squid · aislamiento · colas · video", atk(24), C["muted"], width=W - 96, gap=1.45)
    pie(im); guardar(im, "a5_resultados")

def sin_senal():
    im = lienzo(); y = encabezado(im, "La prueba que no planeamos", "Starlink sin señal, el hub sigue")
    d = ImageDraw.Draw(im)
    b = foto(im, f"{IMG}/f23-foto-starlink.jpeg", (48, y + 10, 330, y + 470), modo="cover")
    text(d, (360, y + 20), "En el laboratorio la antena casi no tuvo vista al cielo.", atk(27), C["paramo"], width=W - 408, gap=1.3)
    vinetas(d, (360, y + 190), ["Portal", "Guías de salud", "Wikipedia", "Videos"], W - 408, size=28, gap=10)
    foto(im, f"{IMG}/f23-offline-starlink-sin-senal.png", (48, b[3] + 40, W - 48, b[3] + 260))
    text(d, (48, b[3] + 290), "Todo respondió por HTTPS sin Internet: para eso se diseñó la red.", bric(28, 650), C["paramo"], width=W - 96)
    pie(im); guardar(im, "a5_sinsenal")

def futuro():
    im = lienzo(); y = encabezado(im, "Fase 3 · Operación en campo", "Lo que falta")
    d = ImageDraw.Draw(im)
    yy = y + 10
    for t, b, col in [("Disco de 2 TB", "Más video, Wikipedia completa y caché de 50 a 100 GB.", C["guadua"]),
                      ("Limpieza automática", "Purga del contenido viejo o poco visto y cuotas por categoría.", C["rio"]),
                      ("Modo en línea / sin conexión", "Conmutación automática y sincronización al volver el enlace.", C["buganvilla"]),
                      ("Batería", "Medición de consumo y apagado ordenado al 15 %.", C["maiz"])]:
        tarjeta(d, (48, yy, W - 48, yy + 165), t, b, col, tsize=30, bsize=25); yy += 185
    text(d, (48, yy + 14), "Nada de esto exige cambiar el diseño, solo ampliarlo.", bric(27, 650), C["paramo"], width=W - 96)
    pie(im); guardar(im, "a5_futuro")

def cierre():
    im = lienzo(); sierra(im, 0, 560)
    d = ImageDraw.Draw(im)
    d.text((48, 630), "Gracias, profesor", font=bric(72), fill=C["paramo"])
    y = text(d, (48, 740), "José David Rodríguez Pinilla\nCarol Andrea Mosquera", bric(34, 600), C["paramo"], gap=1.3)
    y = text(d, (48, y + 20), "Infraestructura de Redes 2 · Universidad Icesi", atk(26), C["muted"])
    y += 40
    rrect(d, (48, y, W - 48, y + 150), 18, fill=C["blanco"], outline=C["line"], width=2)
    d.text((76, y + 26), "Informe, configuraciones y evidencias", font=atk(23), fill=C["muted"])
    d.text((76, y + 70), "github.com/JOSED235/", font=mono(32), fill=C["guadua"])
    d.text((76, y + 106), "ProyectoRedesRurales", font=mono(32), fill=C["guadua"])
    guardar(im, "a5_cierre")

def separador(nombre, kicker, titulo, sub):
    im = lienzo(); sierra(im, 0, 640)
    d = ImageDraw.Draw(im)
    d.text((48, 700), kicker.upper(), font=atk(24, True), fill=C["guadua"])
    y = text(d, (48, 740), titulo, bric(62), C["paramo"], width=W - 96, gap=1.05)
    text(d, (48, y + 16), sub, atk(28), C["muted"], width=W - 96)
    guardar(im, nombre)

# --------- subtítulos (PNG con transparencia, 720x1280) ---------
def subtitulo(nombre, etiqueta, linea, sub=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1, f2 = atk(30, True), atk(24)
    ls = wrap(d, linea, f1, W - 150)
    ss = wrap(d, sub, f2, W - 150) if sub else []
    h = 64 + len(ls) * 38 + (len(ss) * 31 + 8 if ss else 0) + 24
    y0 = H - 80 - h
    d.rounded_rectangle((32, y0, W - 32, H - 80), 22, fill=(23, 59, 47, 232))
    d.rounded_rectangle((32, y0, 44, H - 80), 6, fill=C["maiz"])
    d.text((70, y0 + 22), etiqueta.upper(), font=atk(20, True), fill=C["maiz"])
    y = y0 + 58
    for l in ls: d.text((70, y), l, font=f1, fill="#FFFFFF"); y += 38
    y += 8
    for l in ss: d.text((70, y), l, font=f2, fill="#CFE0D6"); y += 31
    im.save(os.path.join(OUT, nombre + ".png"))

def etiqueta_seccion(nombre, texto, sub):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1, f2 = bric(34), atk(22)
    w = max(d.textlength(texto, font=f1), d.textlength(sub, font=f2)) + 70
    d.rounded_rectangle((32, 60, 32 + w, 180), 20, fill=(23, 59, 47, 232))
    d.rounded_rectangle((32, 60, 44, 180), 6, fill=C["maiz"])
    d.text((66, 82), texto, font=f1, fill="#FFFFFF"); d.text((66, 136), sub, font=f2, fill="#CFE0D6")
    im.save(os.path.join(OUT, nombre + ".png"))

if __name__ == "__main__":
    for fn in [portada, agenda, propuestas, consolidado, gns3, fisico, vlsm, relay, topologia, vlans, troncal, matriz,
               cdn, nginx_dns, squid, flujo, fallas, p12, p13, colas, video, jellyfin, resultados, sin_senal, futuro, cierre]:
        fn()
    separador("sep_demo", "Parte 1", "Demostración en el laboratorio", "Grabado por Carol con la Starlink Mini conectada")
    etiqueta_seccion("e_demo", "Demostración en el laboratorio", "Carol Andrea Mosquera")
    etiqueta_seccion("e_terminal", "Comprobación por terminal", "Raspberry Pi 5 y MikroTik por SSH")
    S = subtitulo
    S("s_ping1", "MikroTik · ping", "192.168.1.1 responde", "Router de la Starlink Mini, conectado a ether9")
    S("s_ping2", "MikroTik · ping", "192.168.100.1 responde", "La antena Starlink")
    S("s_ping3", "MikroTik · ping", "8.8.8.8: tiempo de espera agotado", "Sin vista despejada al cielo no hay salida a Internet")
    S("s_obst", "Starlink Mini", "Señal intermitente", "La antena apunta por la ventana; la palmera la obstruye")
    S("s_offline", "Offline-first", "Sin Internet, el contenido local sigue disponible")
    S("s_ssid", "Celular", "Hub-Salud (WPA2) y Hub-Publica (abierta)", "Un SSID por VLAN, emitidos por el TP-Link")
    S("s_cert", "Certificado", "*.hub.lan firmado por una CA de pruebas propia", "En campo se reemplaza por uno de Let's Encrypt")
    S("s_portal", "Portal sin conexión", "portal.hub.lan", "Documentos, Wikipedia y cursos servidos desde el hub")
    S("s_guias", "Guías propias", "Primeros auxilios y lavado de manos", "Basadas en la IFRC y la OMS")
    S("s_videos", "CDN de video", "portal.hub.lan/videos.html", "Videos 720p servidos desde el disco del hub")
    S("s_serv", "Raspberry · systemctl is-active", "dnsmasq, chrony, nginx, kiwix y squid: active")
    S("s_relay", "MikroTik · DHCP relay", "relay-salud y relay-publica hacia 10.20.0.162")
    S("s_ntp", "MikroTik · NTP", "Sincronizado con la Raspberry (10.20.0.162)", "Sin hora correcta, los certificados HTTPS fallan")
    S("s_fw", "Firewall", "Desde Hub-Publica no se llega a administración")
    print("ok", len(os.listdir(OUT)))
