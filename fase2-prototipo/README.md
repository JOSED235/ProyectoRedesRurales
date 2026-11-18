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

## 2.2 — MikroTik físico

MikroTik **CCR2004-16G-2S+** (RouterOS 7.13.5) del laboratorio, compartido con otro grupo. Se carga el respaldo del hub al empezar y se devuelve el del otro grupo al terminar.

| Puerto | Uso |
|---|---|
| `ether9` | WAN: portátil que comparte su WiFi (simula la Starlink, red `10.42.0.0/24`) |
| `ether10` | Raspberry Pi (acceso VLAN 10) |
| `ether11` | Troncal del AP (VLAN 10 sin etiqueta, 20 y 30 etiquetadas) |
| `ether12` | Portátil de administración (VLAN 10) |
| resto | Deshabilitados |

## 2.3 — Servicios, access point y portal cautivo

Documento: [`Fase2.3_Servicios_AP_Portal_Cautivo.pdf`](Fase2.3_Servicios_AP_Portal_Cautivo.pdf) · Para retomar en el lab: **[`ARRANQUE-LAB.md`](ARRANQUE-LAB.md)**

Respaldo del 17/11/2026: [`configs/mikrotik/hub-ccr2004-2026-11-17.rsc`](../configs/mikrotik/hub-ccr2004-2026-11-17.rsc) y [`configs/servidor/etc/`](../configs/servidor/etc/).

**Decisión:** en el prototipo los servicios del hub se instalan con `apt` y corren con systemd, sin Docker. Así gastan menos RAM, arrancan sin depender de otro servicio y `RequiresMountsFor=/srv/cdn` los protege si falta el disco. Docker queda para la Fase 3 (Jellyfin y Mosquitto), si hace falta.

| Paso | Qué | Dónde | Estado |
|---|---|---|---|
| 1 | ufw, SSH solo con llave, disco en `/srv/cdn` (ext4, `noatime`, `nofail`) | Raspberry | Hecho |
| 2 | dnsmasq (DNS `hub.lan` + DHCP de las 3 VLAN) y relay DHCP | Raspberry, MikroTik | Hecho |
| 3 | chrony como fuente de hora; MikroTik toma la hora de `10.20.0.162` | Raspberry, MikroTik | Hecho |
| 4 | CA de pruebas, certificado `*.hub.lan`, Nginx HTTPS, Kiwix | Raspberry | Hecho |
| 5 | Squid transparente (`3129 intercept`) + PBR `to-proxy` + netwatch | Raspberry, MikroTik | Hecho |
| 6 | TP-Link TL-WA801ND: Hub-Salud (V20, WPA2) y Hub-Publica (V30, abierta) | TP-Link | Hecho |
| 7 | Certificado en el MikroTik y Hotspot | MikroTik | Pendiente |
| 8 | Firewall entre VLAN y colas | MikroTik | Pendiente |
| 9 | Pruebas P1–P15 con capturas | Todos | Pendiente |

El access point de la prueba es el **TP-Link TL-WA801ND** del laboratorio. El UniFi UAP-AC-M sigue siendo el del diseño final; la configuración SSID↔VLAN es la misma.

### Pruebas (evidencia para la rúbrica)

| ID | Criterio | Qué se prueba | Resultado esperado | Estado |
|---|---|---|---|---|
| P1 | Instalación y SO | Todo vuelve tras `sudo reboot` | 5× `active` y `/srv/cdn` con `noatime` | Pendiente |
| P2 | Instalación y SO | Seguridad básica | `Permission denied (publickey)`; ufw activo | Pendiente |
| P3 | Conectividad | DHCP por relay, pública | IP `.10–.126`, gw `10.20.0.1`, DNS `10.20.0.162` | Pendiente |
| P4 | Conectividad | DHCP por relay, salud | IP `.135–.158`, gw `10.20.0.129` | Pendiente |
| P5 | Conectividad | DNS local y caché | `portal.hub.lan` → `10.20.0.162`; 2.ª consulta ≈ 0 ms | Pendiente |
| P6 | Conectividad | Hora común | MikroTik `synchronized` con `10.20.0.162` | Pendiente |
| P7 | Conectividad | Portal cautivo pública | Abre solo; con la prueba se navega | Pendiente |
| P8 | Conectividad | Portal con usuario, salud | Navega; `/ip hotspot active print` | Pendiente |
| P9 | Caché estática | HTTPS obligatorio | `http://portal.hub.lan` termina en HTTPS con candado | Pendiente |
| P10 | Caché estática | Contenido sin iniciar sesión | Portal, PDF y Wikipedia abren | Pendiente |
| P11 | Caché estática | Sin Internet | P5, P9 y P10 siguen funcionando | Pendiente |
| P12 | Caché estática | Caché de Squid | `TCP_MISS` y luego `TCP_HIT`/`TCP_MEM_HIT` | Pendiente |
| P13 | Caché estática | Squid caído no corta | Sigue navegando; `pbr-squid` desactivada | Pendiente |
| P14 | Conectividad | Aislamiento entre VLAN | Desde Hub-Publica, `http://10.20.0.163` no abre | Pendiente |
| P15 | Conectividad | Límite de ancho de banda | ≈ 2 Mbps de bajada por usuario | Pendiente |

### Bitácora (causa → solución)

| Problema | Causa | Solución |
|---|---|---|
| `ssh-copy-id` falla con `Permission denied (publickey)` | El paso 1.3 apagó la contraseña por SSH | Otra persona con acceso agrega la llave a `authorized_keys`, o se activa la contraseña un momento desde la consola local (ver `ARRANQUE-LAB.md`, A.1) |
| `/etc/fstab` con dos montajes en `/srv/cdn` | Se agregó la línea del disco USB sin quitar la del archivo de 10 GB; los dos se llaman `HUBDATA` | Dejar una sola línea (`ARRANQUE-LAB.md`, B.4) |
| El portátil no ve la web del AP | El AP solo responde a su red | NAT de laboratorio `lab: portatil a la web del AP`; se borra al cerrar |
| SSH se cuelga tras `ufw enable` | Faltaba la regla del portátil | `sudo ufw allow from 10.42.0.0/24` desde la consola local |

### Siguiente (Fase 3)

- Disco SSD de 2–4 TB definitivo y Squid con 50–100 GB de caché.
- RTC con pila (`dtparam=rtc_bbat_vchg=3000000`) para tener hora sin Internet tras el apagado al 15 %.
- Certificado real con certbot (DNS-01) cuando el profesor confirme el dominio.

## Rúbrica Fase 2 (objetivo *Accomplished*)

- SO optimizado para discos de 2–4 TB y con seguridad básica.
- Caché rápida de sitios populares y archivos educativos, también offline.
- DHCP/DNS local robusto y portal cautivo básico.
