#!/usr/bin/env python3
"""Convierte texto de terminal (stdin) en una captura PNG con estilo de terminal Ubuntu.

Uso:  (echo 'carol@hub:~$ comando'; comando) | python3 captura.py docs/img/f23-algo.png
Las líneas con un prompt (usuario@host:~$  o  [admin@hub-mikrotik] >) se colorean.
Requiere Pillow.
"""
import re, sys
from PIL import Image, ImageDraw, ImageFont

FUENTE = "/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf"
ALT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONDO, TEXTO, VERDE, AZUL = (48, 10, 36), (238, 238, 236), (138, 226, 52), (114, 159, 207)
PROMPT = re.compile(r"^(\S+@[\w.-]+)(:)([^$\s]*)(\$ ?)|^(\[\S+@[\w.-]+\] > ?)")


def main(salida, tam=17, max_col=150):
    lineas = [l.rstrip("\n").expandtabs(8) for l in sys.stdin]
    while lineas and not lineas[-1].strip():
        lineas.pop()
    partidas = []
    for l in lineas:
        while len(l) > max_col:
            partidas.append(l[:max_col]); l = l[max_col:]
        partidas.append(l)
    try:
        f = ImageFont.truetype(FUENTE, tam)
    except OSError:
        f = ImageFont.truetype(ALT, tam - 2)
    ancho_c = f.getlength("M"); alto = int(tam * 1.3)
    w = int(max(len(l) for l in partidas + [" " * 60]) * ancho_c + 24)
    img = Image.new("RGB", (w, alto * len(partidas) + 16), FONDO)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(partidas):
        x, y = 10, 8 + i * alto
        m = PROMPT.match(l)
        if m:
            if m.group(5):
                trozos = [(m.group(5), VERDE)]
            else:
                trozos = [(m.group(1), VERDE), (m.group(2), TEXTO), (m.group(3), AZUL), (m.group(4), TEXTO)]
            for t, c in trozos:
                d.text((x, y), t, font=f, fill=c); x += f.getlength(t)
            l = l[m.end():]
        d.text((x, y), l, font=f, fill=TEXTO)
    img.save(salida)
    print("captura:", salida, img.size)


if __name__ == "__main__":
    main(sys.argv[1])
