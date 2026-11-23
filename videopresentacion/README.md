# Video de sustentación

| Archivo | Qué es |
|---|---|
| `VideoSustentacion_Final.mp4` | Video entregado (13:21, vertical 720×1280): **[ver en Google Drive](https://drive.google.com/file/d/1J6_ganKjTGxB2m3KPEWVqq3gwkQ7xW5S/view?usp=sharing)**. No está en el repositorio porque pesa 120 MB (GitHub admite hasta 100 MB). |
| `VideoSustentacion.mp4` | Grabación original de Carol en el laboratorio con la Starlink Mini conectada (9:43). Tampoco se versiona. |
| [`GUION-AUDIO-JOSE.md`](GUION-AUDIO-JOSE.md) | Guion de la narración complementaria de José (presentación, diseño, direccionamiento, pruebas y cierre). |
| [`audios/`](audios/) | Narración de José, un archivo por bloque. |
| [`edicion/`](edicion/) | Montaje reproducible: `slides.py` genera las diapositivas con la paleta y las fuentes del portal; `edit.py` limpia y nivela el audio, corta, sincroniza las diapositivas con la voz y une todo con ffmpeg. |

## Estructura del video final

| Tiempo | Parte | Voz |
|---|---|---|
| 0:00 | Presentación y contenido | José |
| 0:28 | Demostración en el laboratorio: equipos, Starlink, celular, portal, guías y videos | Carol |
| 5:23 | De dónde salió el diseño: Fase 1, diseño consolidado, GNS3, paso a lo físico, VLSM y relay DHCP | José |
| 7:05 | Cómo funciona: VLAN, troncal 802.1Q, firewall, CDN, HTTPS/DNS, Squid y tolerancia a fallas | Carol |
| 9:50 | Comprobación por terminal: servicios, relay, NTP y aislamiento | Carol |
| 11:12 | Pruebas complementarias: caché, conmutación de Squid, colas y video con peticiones de rango | José |
| 12:17 | Resultados (15/15 y 4/4), operación sin señal, trabajo futuro y cierre | José |

## Regenerar

```bash
pip install imageio-ffmpeg pillow
cd videopresentacion/edicion
python slides.py          # diapositivas/
python edit.py            # ../VideoSustentacion_Final.mp4 (necesita VideoSustentacion.mp4)
```
