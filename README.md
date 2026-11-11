# Proyecto Redes Rurales — Infraestructura de Redes 2

> **Diseño e implementación de la infraestructura de red local autónoma para una plataforma de atención móvil comunitaria en entornos rurales**
> **Universidad Icesi** — Departamento de Tecnologías de Información y Comunicaciones
> **Materia:** Infraestructura de Redes 2 — **Profesor:** Andrés Navarro Cadavid, Ph.D.
> **Equipo:**
> - José David Rodríguez Pinilla — `A00407151`
> - Carol Andrea Mosquera — `A00403934`

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

Paso de virtual a físico, un equipo a la vez: **2.1** RPi5 física (vía nodo Cloud de GNS3) → **2.2** MikroTik físico (CCR2004 prestado, puertos `ether9`–`ether12`) → AP UniFi → Starlink → energía. Detalle en [`fase2-prototipo/README.md`](fase2-prototipo/README.md).

---

## 3. Arquitectura vigente

### 3.1 Equipos

| Equipo | Rol |
|---|---|
| **Starlink Mini** (modo bypass) | Salida a Internet. Entrega la IP de `ether1` por DHCP y aplica CGNAT. |
| **MikroTik** (RouterOS 7) | Router L3 de todas las VLAN (router-on-a-stick, bridge con `vlan-filtering`), NAT. En Fase 2: firewall entre VLAN, Hotspot (portal cautivo), colas y relay DHCP. |
| **UniFi UAP-AC-M** (PoE) | Access point L2. Asocia cada SSID a una VLAN. Su gestión va sin etiqueta en la VLAN 10. |
| **Raspberry Pi 5** — servidor `hub` | Ubuntu Server 24.04 ARM64 con IP fija en la VLAN 10. Servicios: DNS/DHCP (`dnsmasq`), NTP (`chrony`), Docker, Nginx, Squid, Mosquitto. Disco NVMe + 2–4 TB por USB 3. |
| Portátil de administración | Conectado por cable a `ether4` (VLAN 10). |
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
| 10 | Administración | `10.20.0.160/28` | `10.20.0.161` | 14 | hub `.162`, cliente-admin `.164` |
| 20 | Salud | `10.20.0.128/27` | `10.20.0.129` | 30 | (lab) cliente-salud `.130` |
| 30 | Pública / Comunidad | `10.20.0.0/25` | `10.20.0.1` | 126 | (lab) cliente-publica `.5` |
| — | Libre para crecer | `10.20.0.176/28`, `10.20.0.192/26` | — | 14 + 62 | — |
| WAN | `ether1` | DHCP de Starlink (en GNS3: `192.168.122.0/24`) | — | — | — |

NAT: `srcnat 10.20.0.0/24 → ether1 masquerade`. Hay doble traducción (MikroTik + CGNAT de Starlink). Por eso desde Internet nadie puede iniciar conexiones hacia el sitio.

### 3.4 Configuraciones en el repositorio

- [`configs/mikrotik/hub-base.rsc`](configs/mikrotik/hub-base.rsc): configuración base del MikroTik con los puertos del plan (`ether1`–`ether4`).
- [`configs/mikrotik/hub-ccr2004.rsc`](configs/mikrotik/hub-ccr2004.rsc): la misma configuración en el CCR2004 prestado (`ether9`–`ether12`), más NTP y servicios de gestión.
- [`configs/servidor/01-hub.yaml`](configs/servidor/01-hub.yaml): netplan del hub (RPi5).

---

## 4. Estrategia de caché, almacenamiento y energía

Estas ideas vienen de la versión de José ([`InformePFinal.tex`](fase1-plan/version-jose/InformePFinal.tex)). Hay que ajustarlas al direccionamiento vigente en la Fase 2.

- **Caché Squid jerárquica:** RAM (`cache_mem`), `rock` en NVMe para objetos pequeños y `aufs` en el disco de 2–4 TB para objetos grandes. Reemplazo `heap LFUDA`.
- **HTTPS:** *peek and splice* por SNI, sin instalar una CA en los teléfonos. El contenido masivo se sirve desde espejos locales en Nginx.
- **Refresco:** `refresh_pattern` agresivo para estáticos (`pdf`, `epub`, `zim`, `mp4`, `jpg`, `css`, `js`): mínimo 7 días, máximo 30.
- **Contenido offline:** Kiwix (Wikipedia ZIM), Kolibri y videos pre-transcodificados para Jellyfin.
- **Conmutación online/offline:** *heartbeat* con histéresis que activa `offline_mode` en Squid.
- **Energía:** batería con medidor y apagado ordenado al 15 %. Además: `ext4` con `noatime` y particiones por servicio para evitar corrupción.

---

## 5. Estructura del repositorio

```
ProyectoRedesRurales/
├── docs/                                  # Material oficial del curso
│   ├── Enunciado.txt
│   └── Rúbrica Proyecto Redes Rurales.xlsx
├── fase1-plan/                            # Fase 1 — Plan de proyecto
│   ├── README.md                          # Comparación de versiones y diseño consolidado
│   ├── version-jose/InformePFinal.tex     # Informe IEEE (versión José)
│   ├── version-carol/…Carol.pdf           # Topología, VLSM y enrutamiento (versión Carol)
│   └── laboratorio-gns3/…GNS3_Hub.pdf     # Fase 1.2 — laboratorio virtual consolidado
├── fase2-prototipo/                       # Fase 2 — Prototipo
│   ├── README.md
│   ├── Fase2.1_Implementacion_Fisica_RPi5.pdf
│   └── Fase2.2_MikroTik_CCR2004_Respaldo_Hub_Restauracion.pdf
├── fase3-operacion/README.md              # Fase 3 — Alcance pendiente
├── configs/                               # Configuraciones de equipos (ver configs/README.md)
│   ├── mikrotik/hub-base.rsc              # RouterOS 7 base (puertos del plan)
│   ├── mikrotik/hub-ccr2004.rsc           # RouterOS 7 en el CCR2004 prestado
│   └── servidor/01-hub.yaml               # Netplan del hub RPi5
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
- [x] **Fase 1.2 — Laboratorio virtual GNS3** (27/10/2026)
  - [x] MikroTik CHR 7.25 con VLAN 10/20/30, NAT y salida a Internet.
  - [x] Servidor Ubuntu 24.04.5 en `10.20.0.162/28`, clientes por VLAN y tráfico 802.1Q verificado.
  - [ ] Aislamiento entre VLAN (se hace en la Fase 2 con el firewall).
- [ ] **Fase 2 — Prototipo funcional**
  - [x] 2.1 Raspberry Pi 5 física (Ubuntu Server 24.04) integrada al laboratorio mediante un nodo Cloud.
  - [x] 2.2 MikroTik físico: CCR2004 prestado con la configuración del hub (`ether9`–`ether12`), portátil como WAN, respaldo y restauración del otro grupo (05/11/2026, pruebas 1–10 Cumple).
  - [ ] AP UniFi UAP-AC-M en la troncal.
  - [ ] DHCP/DNS en el hub con relay, Squid, Nginx, Docker y Mosquitto.
  - [ ] Firewall entre VLAN, Hotspot (portal cautivo) y colas.
  - [ ] Disco de 2–4 TB montado y optimizado.
- [ ] **Fase 3 — Sistema plenamente operacional** (Jellyfin, purga automática, dashboard con búsqueda, conmutación online/offline, energía).

---

## 7. Herramientas de IA

- **Claude Code:** la skill [`ingeniero-redes-rurales`](.claude/skills/ingeniero-redes-rurales/SKILL.md) contiene el diseño vigente, el orden de las fuentes de verdad, buenas prácticas de RouterOS/netplan y la rúbrica. Se carga sola en tareas del proyecto o con `/ingeniero-redes-rurales`.
- **Gemini:** [`GEMINI.md`](GEMINI.md).
