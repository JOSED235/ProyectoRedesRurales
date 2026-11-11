# Fase 2 — Prototipo funcional

## 2.1 — Raspberry Pi 5 física dentro del laboratorio

Documento: [`Fase2.1_Implementacion_Fisica_RPi5.pdf`](Fase2.1_Implementacion_Fisica_RPi5.pdf)

La RPi5 reemplaza a la VM `servidor-hub` de GNS3. Se conecta por cable al puerto Ethernet del portátil (`enp46s0`). Un nodo **Cloud** de GNS3 une ese puerto con `ether2` del MikroTik virtual.

Pasos resumidos:

1. Grabar **Ubuntu Server 24.04 LTS (64-bit)** con Raspberry Pi Imager: hostname `hub`, zona `America/Bogota`, SSH activo, sin WiFi. Fuente oficial de 27 W.
2. Actualizar y reiniciar (kernel `6.8.0-1065`).
3. Apagar la VM `servidor-hub` y borrar su cable con `ether2`, para no duplicar `10.20.0.162`.
4. En la RPi: deshabilitar la red de cloud-init y crear [`configs/servidor/01-hub.yaml`](../configs/servidor/01-hub.yaml) (`10.20.0.162/28`, gw `10.20.0.161`). `netplan generate` y luego `netplan apply`. La sesión SSH se corta; es lo esperado.
5. En el portátil: puerto Ethernet con IPv4/IPv6 **desactivado**. Así no hay un segundo DHCP/NAT (`10.42.0.x`) en la VLAN 10.
6. En GNS3: nodo Cloud `raspberry-fisica` (`enp46s0`) conectado a `MikroTik` (`ether2`).
7. Pruebas desde `cliente-admin` y desde la RPi: `ping 10.20.0.162`, `ssh carol@10.20.0.162`, `ping 10.20.0.161`, `ping 8.8.8.8`, `ping ubuntu.com`, `apt update`, `timedatectl`. Desde el portátil: `sudo ip route replace 10.20.0.0/24 via <IP ether1 MikroTik>`.

## 2.2 — MikroTik físico (CCR2004 prestado)

Documento: [`Fase2.2_MikroTik_CCR2004_Respaldo_Hub_Restauracion.pdf`](Fase2.2_MikroTik_CCR2004_Respaldo_Hub_Restauracion.pdf)

Etapa 2 del paso a lo físico: el MikroTik deja de ser el CHR de GNS3 y la RPi5 se conecta directo al router, sin nodo Cloud. Se usa un **CCR2004-16G-2S+** (`sw01`) que pertenece a otro grupo, así que cada sesión empieza respaldando su configuración y termina restaurándola. Direccionamiento igual al de la Fase 1.2 (`10.20.0.0/24`, gateways `.161`, `.129`, `.1`).

Configuración aplicada: [`configs/mikrotik/hub-ccr2004.rsc`](../configs/mikrotik/hub-ccr2004.rsc).

### Plan de puertos

`ether1` y `ether2` tienen el kit y el AP del otro grupo, por eso el hub usa `ether9`–`ether12` (deshabilitados en la configuración del otro grupo). Con un MikroTik propio se vuelve a `ether1`–`ether4`.

| Puerto CCR2004 | Equipo | Modo / VLAN | En GNS3 | En la red final |
|---|---|---|---|---|
| `ether9` | Portátil en modo *Compartida* (simula Starlink) | WAN, cliente DHCP (`10.42.0.0/24`), fuera del bridge | `ether1` → nodo NAT | `ether1` → Starlink Mini |
| `ether10` | Raspberry Pi 5 (`hub`) | Acceso VLAN 10 | `ether2` → VM / nodo Cloud | `ether2` |
| `ether11` | UniFi UAP-AC-M (cuando esté) | Troncal: V10 sin etiqueta, V20/V30 etiquetadas | `ether3` → switch | `ether3` |
| `ether12` | Portátil de administración (opcional) | Acceso VLAN 10 | `ether4` → Alpine | `ether4` |
| `ether1`–`ether8`, `ether13`–`ether16`, SFP+ | Equipos del otro grupo o nada | Deshabilitados | — | — |

### Procedimiento por sesión

| Parte | Qué se hace |
|---|---|
| **A — Respaldo del otro grupo** | `/system backup save` + `/export show-sensitive` con la fecha del día. Portátil en `ether4` con IP manual `10.20.10.20/24` (rango SSH permitido `10.20.10.10`–`.31`), `scp` desde `10.20.10.2`, verificación (`wc -l`, sección `/interface bridge port`) y ZIP con `LEEME-restauracion.txt` enviado al otro grupo. |
| **C — Configuración del hub** | `/system reset-configuration no-defaults=yes skip-backup=yes` y pegado por consola serial **en 5 bloques** (identidad/hora, puertos, bridge/VLAN, IP/DHCP-client/DNS/NAT/NTP, servicios). |
| **D — Portátil como WAN** | Portátil (`enp46s0`) en `ether9` con IPv4 *Compartida con otros equipos* (`10.42.0.1/24`); RPi5 en `ether10` sin cambios. Gestión: `sudo ip route replace 10.20.0.0/24 via <IP de ether9>`. |
| **E — Antes de irse** | `/export` + `/system backup save` del hub y `scp` al portátil; `/system backup load` del respaldo del otro grupo (plan B: `run-after-reset=<.rsc>`); verificar `sw01`, `10.20.10.2/24`, VLAN 10/20/40; borrar archivos `hub-ccr2004*` del equipo y desconectar cables. |

### Pruebas (en orden)

| # | Dónde | Comando | Esperado | Resultado |
|---|---|---|---|---|
| 1 | MikroTik | `/interface print` | `ether9`/`ether10` con R; solo `ether9`–`ether12` sin X | Cumple |
| 2 | MikroTik | `/ip dhcp-client print` | `bound`, IP `10.42.0.x` | Cumple |
| 3 | MikroTik | `/ping 8.8.8.8 count=3` | Responde | Cumple |
| 4 | MikroTik | `/ping 10.20.0.162 count=3` | Responde la RPi5 | Cumple |
| 5 | MikroTik | `/interface bridge host print where on-interface=ether10` | MAC de la RPi5 en VLAN 10 | Cumple |
| 6 | RPi5 | `ping -c 3 10.20.0.161` | Responde el MikroTik | Cumple |
| 7 | RPi5 | `ping -c 3 8.8.8.8` y `ping -c 3 ubuntu.com` | Internet y DNS | Cumple |
| 8 | RPi5 | `sudo apt update` | Sin errores | Cumple |
| 9 | Portátil | `ssh admin@10.20.0.161`, `ssh carol@10.20.0.162` | Entra a ambos | Cumple |
| 10 | MikroTik | `/ip firewall nat print stats` | Contador del masquerade sube | Cumple |

### Bitácora de problemas (causa → solución)

| Síntoma | Causa | Solución |
|---|---|---|
| `NO-CARRIER` en un puerto | Puerto deshabilitado (X) | Usar un puerto habilitado; con la config del otro grupo, `ether4`–`ether8` |
| `scp` a `10.20.10.2` no responde | IP del portátil fuera del rango SSH permitido | IP entre `10.20.10.10` y `10.20.10.31` |
| Letras faltantes al pegar | Mucho texto de golpe por consola serial | Pegar por bloques y revisar cada resultado |
| `ether9` en `searching` | Portátil no está en *Compartida* o cable en otro puerto | Revisar IPv4 y cable; `/ip dhcp-client renew 0` |
| IP en `ether9` pero sin ping a `8.8.8.8` | Portátil sin Internet por WiFi | Revisar WiFi |
| RPi5 no responde | Cable fuera de `ether10` o IP distinta | `ip -br addr show eth0` debe dar `10.20.0.162/28` |
| Portátil no llega a `10.20.0.161` | Falta ruta o cambió la IP de `ether9` | Repetir `ip route replace` con la IP actual |
| SSH: `REMOTE HOST IDENTIFICATION HAS CHANGED` | Huella de la VM anterior | `ssh-keygen -R 10.20.0.162` |
| `backup load` rechaza la contraseña | Contraseña equivocada | Usar la anotada en A1; si no, plan B con el `.rsc` |
| Sin acceso por red | Normal tras reset o cambio de config | Consola serial (`/dev/ttyUSB0`, 115200) |

> **Nota de laboratorio:** cuando se cargue el firewall, hay que aceptar la gestión desde `10.42.0.1` (portátil). Esa regla es solo del laboratorio y no se lleva a la Starlink real.

## Siguiente

- Servicios en el hub: `dnsmasq` (DHCP con relay del MikroTik + DNS), `chrony`, Docker, Nginx, Squid, Mosquitto.
- Firewall entre VLAN, Hotspot (portal cautivo) y colas en el MikroTik.
- AP UniFi en `ether11` (SSID Hub-Salud → V20, Hub-Publica → V30).
- Disco 2–4 TB por USB 3, NVMe con HAT, temperatura (`vcgencmd measure_temp`) y consumo.

## Rúbrica Fase 2 (objetivo *Accomplished*)

- SO optimizado para discos de 2–4 TB y con seguridad básica.
- Caché rápida de sitios populares y archivos educativos, también offline.
- DHCP/DNS local robusto y portal cautivo básico.
