# Fase 1 — Plan de proyecto

Al terminar la Fase 1 cada integrante tenía su propia versión del plan. Luego se unificaron en el diseño consolidado que se validó en el laboratorio GNS3 (Fase 1.2). Se conservan las tres piezas para trazabilidad.

| Carpeta | Autor | Contenido | Estado |
|---|---|---|---|
| [`version-jose/`](version-jose/) | José David Rodríguez | `InformePFinal.tex` — informe IEEE (Overleaf): RPi5, red `10.10.0.0/16`, uplink LTE, portal `openNDS`, estrategia de caché Squid (RAM/NVMe/SSD, peek-and-splice, `refresh_pattern`), energía LiFePO₄, cronograma de 11 semanas, BOM y matriz de riesgos. | Histórico. Reutilizable: caché, almacenamiento, riesgos y cronograma. |
| [`version-carol/`](version-carol/) | Carol Andrea Mosquera | PDF *Topología, direccionamiento IP y enrutamiento*: bloque `10.20.0.0/22`, 4 VLAN (10 Gestión, 20 Personal, 30 Comunidad, 40 Invitados, 999 nativa), VLSM con fórmulas, supernetting (`/23`, `/22`, `/20` multisitio), tablas de rutas, túnel WireGuard, matriz de tráfico entre VLAN. | Histórico. Reutilizable: método VLSM, sumarización, matriz de tráfico. |
| [`laboratorio-gns3/`](laboratorio-gns3/) | Equipo | PDF *Fase 1.2 — Virtual en GNS3 (Hub)*: diseño **consolidado** montado y probado en GNS3 2.2.61 con MikroTik CHR 7.25 + Ubuntu Server 24.04.5. | **Vigente.** |

## Diferencias principales entre versiones

| Aspecto | Versión José | Versión Carol | **Consolidado (vigente)** |
|---|---|---|---|
| Router L3 | Raspberry Pi 5 (nftables) | Mini PC i5 (router-on-a-stick) | **MikroTik RouterOS 7** (router-on-a-stick) |
| Servidor | RPi5 | Mini PC i5 | **RPi5 "hub"**, Ubuntu Server 24.04, IP fija en VLAN 10 |
| WAN | Router LTE | Router 4G + WireGuard | **Starlink Mini** (bypass, CGNAT) |
| AP | Wi-Fi 6 genérico | 3 AP PoE | **UniFi UAP-AC-M** |
| Bloque | `10.10.0.0/16` | `10.20.0.0/22` | **`10.20.0.0/24`** |
| VLAN | 10 Salud, 30 Portal, 99 Gestión, 20 reserva | 10 Gestión, 20 Personal, 30 Comunidad, 40 Invitados | **10 Administración, 20 Salud, 30 Pública** |

## Laboratorio GNS3 (1.2) — resultado

Pruebas del 27/10/2026: salida a Internet del MikroTik, VLAN 10/20/30 en el bridge, servidor con `10.20.0.162/28`, DNS, navegación desde clientes de salud y pública, pruebas A1–A11 del cliente admin y etiquetas 802.1Q en Wireshark → **Cumple**. Aislamiento entre VLAN → **Pendiente (Fase 2, firewall)**.

Configuraciones extraídas: [`configs/mikrotik/hub-base.rsc`](../configs/mikrotik/hub-base.rsc) y [`configs/servidor/01-hub.yaml`](../configs/servidor/01-hub.yaml).
