# Proyecto Redes Rurales — Infraestructura de Redes 2

> **Diseño e implementación de la infraestructura de red local autónoma para una plataforma de atención móvil comunitaria en entornos rurales**
> **Universidad Icesi** — Departamento de Tecnologías de Información y Comunicaciones
> **Materia:** Infraestructura de Redes 2 — **Profesor:** Andrés Navarro Cadavid, Ph.D.
> **Equipo:**
> - José David Rodríguez Pinilla — `A00407151`
> - Carol Andrea Mosquera — `A00403934`

---

## Entregables finales

| Entregable | Dónde |
|---|---|
| **Informe final IEEE (Fases 1 a 2.4 y evaluación frente a la rúbrica)** | [`docs/InformeFinal.pdf`](docs/InformeFinal.pdf) · fuente [`docs/InformeFinal.tex`](docs/InformeFinal.tex) |
| **Video de sustentación (13:21)** | [Ver en Google Drive](https://drive.google.com/file/d/1J6_ganKjTGxB2m3KPEWVqq3gwkQ7xW5S/view?usp=sharing) · estructura, guion y montaje en [`videopresentacion/`](videopresentacion/README.md) |
| Configuraciones reales de los equipos | [`configs/`](configs/README.md) |
| Evidencias (capturas y fotos) | [`docs/img/`](docs/img/) |
| Registro de decisiones | [`docs/DECISIONES.md`](docs/DECISIONES.md) |
| Informe de avance (19/11, histórico) | [`docs/InformeAvance.pdf`](docs/InformeAvance.pdf) |

**Resultado:** las 15 pruebas de red y servicios (P1–P15) y las 4 de video (V1–V4) se cumplieron en hardware físico (MikroTik CCR2004, Raspberry Pi 5, TP-Link y Starlink Mini). Con la Starlink conectada pero sin señal, el portal, los documentos, la Wikipedia y los videos siguieron funcionando.

---

## 1. Contexto

El proyecto despliega la infraestructura para una **unidad de atención comunitaria** que opera en zonas rurales. Allí la conexión a Internet es escasa o costosa y la energía es inestable. El enunciado ([`docs/Enunciado.txt`](docs/Enunciado.txt)) pide:

- Un portal cautivo que dé acceso a cada grupo de interés como si fuera una red independiente con Internet.
- Un proxy/caché local sobre una Mini PC o una Raspberry Pi.

La red sigue la filosofía **offline-first**: los servicios locales funcionan sin Internet. El enlace satelital se usa para navegar y para sincronizar cuando está disponible.

La evaluación usa la rúbrica de 3 fases ([`docs/Rúbrica Proyecto Redes Rurales.xlsx`](docs/Rúbrica%20Proyecto%20Redes%20Rurales.xlsx)): plan, prototipo y sistema operacional.

---

## 2. Historia del diseño

Al cerrar la Fase 1 cada integrante tenía su propia versión del plan. Las dos se unificaron en un **diseño consolidado**, que se montó y validó en GNS3 antes de comprar hardware. El detalle y la comparación están en [`fase1-plan/README.md`](fase1-plan/README.md).

| Versión | Ubicación | Estado |
|---|---|---|
| José (`10.10.0.0/16`, RPi5 como router, LTE, openNDS) | `fase1-plan/version-jose/` | Histórico (se reutilizan caché, almacenamiento, riesgos y cronograma) |
| Carol (`10.20.0.0/22`, Mini PC, 4G, WireGuard) | `fase1-plan/version-carol/` | Histórico (se reutilizan VLSM, sumarización y matriz de tráfico) |
| **Consolidado** (`10.20.0.0/24`, MikroTik + RPi5 + Starlink + UniFi) | `fase1-plan/laboratorio-gns3/`, `fase2-prototipo/` | **Vigente** |

Paso de virtual a físico, un equipo a la vez: **2.1** RPi5 física (vía nodo Cloud de GNS3) → **2.2** MikroTik físico (CCR2004 prestado, puertos `ether9`–`ether12`) → **2.3** servicios del hub, AP (TP-Link de laboratorio), Hotspot, firewall, colas y Starlink Mini → **2.4** CDN local de video. Queda para la operación en campo (Fase 3): AP UniFi, SSD de 2 TB, purga automática y energía. Detalle en [`fase2-prototipo/README.md`](fase2-prototipo/README.md).

---

## 3. Arquitectura vigente

### 3.1 Equipos

| Equipo | Rol |
|---|---|
| **Starlink Mini** (modo bypass en campo; modo normal en el laboratorio) | Salida a Internet. Entrega la IP de `ether1` por DHCP y aplica CGNAT. En el laboratorio se conectó a `ether9` y recibió `192.168.1.159/24`. |
| **MikroTik** (RouterOS 7) | Router L3 de todas las VLAN (router-on-a-stick, bridge con `vlan-filtering`), NAT, relay DHCP, desvío de HTTP a Squid, Hotspot (portal cautivo) con HTTPS, firewall entre VLAN y colas. En el laboratorio es un CCR2004-16G-2S+ compartido (puertos en [`fase2-prototipo/README.md`](fase2-prototipo/README.md#22--mikrotik-físico-ccr2004-prestado)). |
| **UniFi UAP-AC-M** (PoE) | Access point L2. Asocia cada SSID a una VLAN. Su gestión va sin etiqueta en la VLAN 10. En el laboratorio se usa un TP-Link TL-WA801ND (`10.20.0.163`) con la misma configuración. |
| **Raspberry Pi 5** — servidor `hub` | Ubuntu Server 24.04 ARM64 con IP fija en la VLAN 10. Servicios con `apt` + systemd (sin Docker): DNS/DHCP (`dnsmasq`), NTP (`chrony`), Nginx (HTTPS, portal y CDN de video con peticiones de rango), Kiwix, Squid y ufw. Disco USB de 465 GB en `/srv/cdn` en el prototipo; SSD de 2–4 TB en la operación en campo. Jellyfin se descartó: la RPi5 no tiene codificador H.264 por hardware, así que el video se codifica una vez fuera del hub y se sirve como archivo. |
| Portátil de administración | Conectado por cable a `ether4` (VLAN 10); en el CCR2004 del laboratorio, `ether12`. |
| Batería + medidor + convertidores DC | Alimentación autónoma con apagado ordenado al 15 %. |

### 3.2 Topología

```
        [ Internet ] ── Starlink Mini (bypass, CGNAT)
                              │ ether1 (WAN, DHCP)
                    ┌─────────┴─────────┐
                    │  MikroTik  br-lan │  vlan10-admin  10.20.0.161/28
                    │  RouterOS 7       │  vlan20-salud  10.20.0.129/27
                    │                   │  vlan30-publica 10.20.0.1/25
                    └──┬───────┬─────┬──┘
              ether2   │ ether3│     │ ether4        (ether5 deshabilitado)
          (acceso V10) │(troncal)    │(acceso V10)
                       │       │     │
     Raspberry Pi 5 "hub"      │   Portátil admin
       10.20.0.162/28          │
                     UniFi UAP-AC-M  (V10 sin etiqueta + V20/V30 etiquetadas)
                      /                 \
            SSID Hub-Salud (V20)   SSID Hub-Publica (V30)
             teléfonos de salud     teléfonos de la comunidad
```

### 3.3 Direccionamiento (VLSM sobre `10.20.0.0/24`)

| VLAN | Nombre | Subred | Gateway | Hosts útiles | Equipos con IP fija |
|---|---|---|---|---|---|
| 10 | Administración | `10.20.0.160/28` | `10.20.0.161` | 14 | hub `.162`, AP `.163`, cliente-admin `.164` |
| 20 | Salud | `10.20.0.128/27` | `10.20.0.129` | 30 | (lab) cliente-salud `.130` |
| 30 | Pública / Comunidad | `10.20.0.0/25` | `10.20.0.1` | 126 | (lab) cliente-publica `.5` |
| — | Libre para crecer | `10.20.0.176/28`, `10.20.0.192/26` | — | 14 + 62 | — |
| WAN | `ether1` | DHCP de Starlink (en GNS3: `192.168.122.0/24`) | — | — | — |

NAT: `srcnat 10.20.0.0/24 → ether1 masquerade`. Hay doble traducción (MikroTik + CGNAT de Starlink). Por eso desde Internet nadie puede iniciar conexiones hacia el sitio.

### 3.4 Configuraciones en el repositorio

- [`configs/mikrotik/hub-base.rsc`](configs/mikrotik/hub-base.rsc): configuración base del MikroTik (VLAN, gateways, DNS, NAT).
- [`configs/mikrotik/hub-ccr2004.rsc`](configs/mikrotik/hub-ccr2004.rsc): configuración inicial de la Fase 2.2 en el CCR2004 prestado (`ether9`–`ether12`), más NTP y servicios de gestión.
- [`configs/mikrotik/hub-ccr2004-2026-11-17.rsc`](configs/mikrotik/hub-ccr2004-2026-11-17.rsc): `/export` real del MikroTik físico (17/11/2026).
- [`configs/mikrotik/hub-ccr2004-2026-11-18.rsc`](configs/mikrotik/hub-ccr2004-2026-11-18.rsc): `/export` con Hotspot, firewall y colas (18/11/2026).
- [`configs/mikrotik/hub-ccr2004-2026-11-19.rsc`](configs/mikrotik/hub-ccr2004-2026-11-19.rsc): `/export` final (19/11/2026) con la Starlink Mini en `ether9`.
- [`configs/mikrotik/fase23-pendiente.rsc`](configs/mikrotik/fase23-pendiente.rsc): script con el que se aplicaron el Hotspot, el firewall y las colas.
- [`configs/mikrotik/hotspot/`](configs/mikrotik/hotspot/): páginas del Hotspot en español (acceso, estado, cierre de sesión, errores).
- [`configs/servidor/01-hub.yaml`](configs/servidor/01-hub.yaml): netplan del hub (RPi5).
- [`configs/servidor/etc/`](configs/servidor/etc/): dnsmasq, chrony, SSH, Nginx, Squid y Kiwix del hub.
- [`configs/servidor/www/`](configs/servidor/www/): portal `portal.hub.lan` (categorías y búsqueda local), guía del certificado y CA de pruebas.
- [`configs/servidor/contenido/`](configs/servidor/contenido/): scripts que generan las guías PDF propias (`guias.py`) y las fábulas de Samaniego (`fab.py`).

Para retomar en el laboratorio: [`fase2-prototipo/ARRANQUE-LAB.md`](fase2-prototipo/ARRANQUE-LAB.md).

---

## 4. Estrategia de caché, almacenamiento y energía

Plan de la Fase 1 (versión de José, [`InformePFinal.tex`](fase1-plan/version-jose/InformePFinal.tex)). Lo que ya está implementado en el prototipo se resume al final de la sección.

- **Caché Squid jerárquica:** RAM (`cache_mem`), `rock` en NVMe para objetos pequeños y `aufs` en el disco de 2–4 TB para objetos grandes. Reemplazo `heap LFUDA`.
- **HTTPS:** *peek and splice* por SNI, sin instalar una CA en los teléfonos. El contenido masivo se sirve desde espejos locales en Nginx.
- **Refresco:** `refresh_pattern` agresivo para estáticos (`pdf`, `epub`, `zim`, `mp4`, `jpg`, `css`, `js`): mínimo 7 días, máximo 30.
- **Contenido offline:** Kiwix (Wikipedia ZIM), Kolibri y videos pre-transcodificados para Jellyfin (en el prototipo, Jellyfin se reemplazó por Nginx; ver Fase 2.4).
- **Conmutación online/offline:** *heartbeat* con histéresis que activa `offline_mode` en Squid.
- **Energía:** batería con medidor y apagado ordenado al 15 %. Además: `ext4` con `noatime` y particiones por servicio para evitar corrupción.

**Implementado en el prototipo:** Squid transparente (`3129 intercept`) con 256 MB de RAM, 4 GB en disco, `heap LFUDA` y `refresh_pattern` por tipo; HTTPS sin descifrar (sale directo); desvío por PBR en el MikroTik con *netwatch* que lo apaga si Squid cae; Kiwix, PDF y video servidos por Nginx desde `/srv/cdn` (ext4, `noatime,nofail`). **Pendiente (Fase 3):** SSD de 2 TB, caché de 50–100 GB, purga automática, `offline_mode` con *heartbeat* y batería.

---

## 5. Estructura del repositorio

```
ProyectoRedesRurales/
├── docs/                                  # Material del curso, informes y evidencias
│   ├── Enunciado.txt
│   ├── Rúbrica Proyecto Redes Rurales.xlsx
│   ├── InformeFinal.tex / .pdf            # ► Informe final IEEE (entrega)
│   ├── InformeAvance.tex / .pdf           # Informe de avance (Fases 1 a 2.3, 19/11/2026)
│   ├── DECISIONES.md                      # Registro de decisiones y datos importantes (con fecha)
│   ├── GUION-VIDEO.md                     # Guion del video de la demostración
│   ├── captura.py                         # Convierte salida de terminal en PNG para las evidencias
│   └── img/                               # Capturas y fotos de evidencia usadas en los informes
├── fase1-plan/                            # Fase 1 — Plan de proyecto
│   ├── README.md                          # Comparación de versiones y diseño consolidado
│   ├── version-jose/InformePFinal.tex     # Informe IEEE (versión José)
│   ├── version-carol/…Carol.pdf           # Topología, VLSM y enrutamiento (versión Carol)
│   └── laboratorio-gns3/…GNS3_Hub.pdf     # Fase 1.2 — laboratorio virtual consolidado
├── fase2-prototipo/                       # Fase 2 — Prototipo
│   ├── README.md                          # 2.1, 2.2, 2.3, pruebas y bitácora
│   ├── ARRANQUE-LAB.md                    # Lista para retomar en el laboratorio
│   ├── SESION-2026-11-18.md               # Bitácora de la sesión del 18/11
│   ├── SESION-2026-11-19.md               # Bitácora del 19/11 (Starlink, P12/P13, contenido)
│   ├── GUIA-GRABACION-VIDEO.md            # Clips del laboratorio para el video
│   ├── Fase2.1_Implementacion_Fisica_RPi5.pdf
│   ├── Fase2.2_MikroTik_CCR2004_Respaldo_Hub_Restauracion.pdf
│   └── Fase2.3_Servicios_AP_Portal_Cautivo.pdf
├── videopresentacion/                     # Guion, narración y montaje del video (el .mp4 está en Drive)
├── fase3-operacion/README.md              # Fase 3 — Hecho (video, portal) y pendiente
├── configs/                               # Configuraciones de equipos (ver configs/README.md)
│   ├── mikrotik/                          # hub-base (GNS3), exports del CCR2004, páginas del Hotspot
│   └── servidor/                          # Netplan, /etc, portal web y scripts de contenido del hub
├── skills/skills.md                       # Catálogo de competencias del proyecto
├── .claude/skills/ingeniero-redes-rurales/SKILL.md   # Skill de Claude Code (ingeniero de redes)
├── GEMINI.md                              # Reglas del asistente (siempre en español)
└── README.md
```

---

## 6. Estado del proyecto

- [x] **Fase 1 — Plan de proyecto**
  - [x] Versión José: informe IEEE con caché, almacenamiento, cronograma, BOM y riesgos.
  - [x] Versión Carol: topología, VLSM, supernetting, tablas de rutas y matriz de tráfico.
  - [x] Diseño consolidado (MikroTik + RPi5 + Starlink + UniFi, `10.20.0.0/24`).
- [x] **Fase 1.2 — Laboratorio virtual GNS3** (27/10/2026): VLAN 10/20/30, NAT, clientes por VLAN y 802.1Q verificado en Wireshark.
- [x] **Fase 2 — Prototipo funcional**
  - [x] 2.1 Raspberry Pi 5 física integrada al laboratorio mediante un nodo Cloud (30/10/2026).
  - [x] 2.2 MikroTik físico CCR2004 prestado (`ether9`–`ether12`), respaldo y restauración del otro grupo (05/11/2026, pruebas 1–10).
  - [x] 2.3 Hub: ufw, SSH con llave, `/srv/cdn`, dnsmasq + relay, chrony, Nginx HTTPS, Kiwix, Squid transparente (13–17/11).
  - [x] 2.3 AP TP-Link (Hub-Salud V20, Hub-Publica V30), Hotspot por VLAN, firewall de 18 reglas y colas (18/11).
  - [x] 2.3 Portal rediseñado, guías PDF, páginas del Hotspot en español y Starlink Mini en `ether9` (19/11).
  - [x] 2.4 CDN local de video: MP4 720p ≤ 1,2 Mbps con *faststart*, Nginx con peticiones de rango (206) y catálogo `videos.html` (20/11).
  - [x] Pruebas P1–P15 y V1–V4: todas Cumple (detalle en la Tabla VII del informe final).
- [x] Informe final IEEE: [`docs/InformeFinal.pdf`](docs/InformeFinal.pdf) (compilado con `texlive/texlive:latest-full`).
- [ ] **Fase 3 — Operación en campo** (ver [`fase3-operacion/README.md`](fase3-operacion/README.md)): hecho el streaming local y el portal con búsqueda; falta SSD de 2–4 TB, purga automática y cuotas, conmutación online/offline, batería y AP UniFi.

### Compilar el informe

```bash
cd docs
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/w -w /w texlive/texlive:latest-full \
  latexmk -pdf -interaction=nonstopmode InformeFinal.tex
latexmk -c InformeFinal.tex   # borra los auxiliares
```

---

## 7. Herramientas de IA

**Documentar al momento:** toda decisión, cambio de decisión o dato importante (IP, puerto, versión, fecha, resultado de prueba, problema y causa) se anota en el mismo momento en [`docs/DECISIONES.md`](docs/DECISIONES.md) con fecha, porqué y dónde quedó; luego se actualizan los README y el informe. Sin contraseñas ni llaves.

- **Claude Code:** la skill [`ingeniero-redes-rurales`](.claude/skills/ingeniero-redes-rurales/SKILL.md) contiene el diseño vigente, el orden de las fuentes de verdad, buenas prácticas de RouterOS/netplan y la rúbrica. Se carga sola en tareas del proyecto o con `/ingeniero-redes-rurales`.
- **Gemini:** [`GEMINI.md`](GEMINI.md).
