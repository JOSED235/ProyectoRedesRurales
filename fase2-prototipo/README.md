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

Documento: [`Fase2.3_Servicios_AP_Portal_Cautivo.pdf`](Fase2.3_Servicios_AP_Portal_Cautivo.pdf) · Para retomar en el lab: **[`ARRANQUE-LAB.md`](ARRANQUE-LAB.md)** · Sesión del 18/11: **[`SESION-2026-11-18.md`](SESION-2026-11-18.md)**

Respaldo del 17/11/2026: [`configs/mikrotik/hub-ccr2004-2026-11-17.rsc`](../configs/mikrotik/hub-ccr2004-2026-11-17.rsc) y [`configs/servidor/etc/`](../configs/servidor/etc/).
Estado del 18/11/2026 (pasos 7 y 8 aplicados): [`configs/mikrotik/hub-ccr2004-2026-11-18.rsc`](../configs/mikrotik/hub-ccr2004-2026-11-18.rsc) y [`configs/mikrotik/hotspot/login.html`](../configs/mikrotik/hotspot/login.html). Bridge, VLAN 10/20/30, puertos, IPs, relay, NAT y PBR quedaron iguales al 17/11; solo se agregó lo de los pasos 7 y 8.
Rediseño del 19/11 (sin laboratorio): portal [`configs/servidor/www/index.html`](../configs/servidor/www/index.html) con categorías Educación/Salud/Ocio y búsqueda local, guía [`certificado.html`](../configs/servidor/www/certificado.html) y todas las páginas del Hotspot en español en [`configs/mikrotik/hotspot/`](../configs/mikrotik/hotspot/). Se suben con [`ARRANQUE-LAB.md`](ARRANQUE-LAB.md) C.3.

**Decisión:** en el prototipo los servicios del hub se instalan con `apt` y corren con systemd, sin Docker. Así gastan menos RAM, arrancan sin depender de otro servicio y `RequiresMountsFor=/srv/cdn` los protege si falta el disco. Docker queda para la Fase 3 (Jellyfin y Mosquitto), si hace falta.

| Paso | Qué | Dónde | Estado |
|---|---|---|---|
| 1 | ufw, SSH solo con llave, disco en `/srv/cdn` (ext4, `noatime`, `nofail`) | Raspberry | Hecho |
| 2 | dnsmasq (DNS `hub.lan` + DHCP de las 3 VLAN) y relay DHCP | Raspberry, MikroTik | Hecho |
| 3 | chrony como fuente de hora; MikroTik toma la hora de `10.20.0.162` | Raspberry, MikroTik | Hecho |
| 4 | CA de pruebas, certificado `*.hub.lan`, Nginx HTTPS, Kiwix | Raspberry | Hecho |
| 5 | Squid transparente (`3129 intercept`) + PBR `to-proxy` + netwatch | Raspberry, MikroTik | Hecho |
| 6 | TP-Link TL-WA801ND: Hub-Salud (V20, WPA2) y Hub-Publica (V30, abierta) | TP-Link | Hecho |
| 7 | Certificado en el MikroTik, Hotspot y enlace en `login.html` | MikroTik | Hecho (18/11) |
| 8 | Firewall entre VLAN y colas | MikroTik | Hecho y comprobado (18/11) |
| 9 | Pruebas P1–P15 con capturas | Todos | En curso (11/15 el 18/11) |
| 10 | Portal rediseñado, guía del certificado y páginas del Hotspot; `host-record` de `wifi-publica`/`wifi-salud`; `certificado.html` por HTTP en Nginx | Raspberry, MikroTik | En el repo (19/11); falta subir y probar |

El access point de la prueba es el **TP-Link TL-WA801ND** del laboratorio. El UniFi UAP-AC-M sigue siendo el del diseño final; la configuración SSID↔VLAN es la misma.

### Pruebas (evidencia para la rúbrica)

| ID | Criterio | Qué se prueba | Resultado esperado | Estado |
|---|---|---|---|---|
| P1 | Instalación y SO | Todo vuelve tras `sudo reboot` | 5× `active` y `/srv/cdn` con `noatime` | Pendiente |
| P2 | Instalación y SO | Seguridad básica | `Permission denied (publickey)`; ufw activo | OK 18/11 (se volvió a poner `PasswordAuthentication no`) |
| P3 | Conectividad | DHCP por relay, pública | IP `.10–.126`, gw `10.20.0.1`, DNS `10.20.0.162` | OK 18/11 (`10.20.0.57`) |
| P4 | Conectividad | DHCP por relay, salud | IP `.135–.158`, gw `10.20.0.129` | OK 18/11 (`10.20.0.157`) |
| P5 | Conectividad | DNS local y caché | `portal.hub.lan` → `10.20.0.162`; 2.ª consulta ≈ 0 ms | OK 18/11 (12 ms → 0 ms) |
| P6 | Conectividad | Hora común | MikroTik `synchronized` con `10.20.0.162` | OK 18/11 |
| P7 | Conectividad | Portal cautivo pública | Abre solo; con la prueba se navega | OK 18/11 |
| P8 | Conectividad | Portal con usuario, salud | Navega; `/ip hotspot active print` | OK 18/11 (falta captura de `active print`) |
| P9 | Caché estática | HTTPS obligatorio | `http://portal.hub.lan` termina en HTTPS con candado | OK 18/11 (301 → HTTPS, verificado con la CA) |
| P10 | Caché estática | Contenido sin iniciar sesión | Portal, PDF y Wikipedia abren | Pendiente |
| P11 | Caché estática | Sin Internet | P5, P9 y P10 siguen funcionando | OK 18/11 (WiFi del portátil apagado) |
| P12 | Caché estática | Caché de Squid | `TCP_MISS` y luego `TCP_HIT`/`TCP_MEM_HIT` | Pendiente |
| P13 | Caché estática | Squid caído no corta | Sigue navegando; `pbr-squid` desactivada | Pendiente |
| P14 | Conectividad | Aislamiento entre VLAN | Desde Hub-Publica, `http://10.20.0.163` no abre | OK 18/11 |
| P15 | Conectividad | Límite de ancho de banda | ≈ 2 Mbps de bajada por usuario | OK 18/11 |

### Bitácora (causa → solución)

| Problema | Causa | Solución |
|---|---|---|
| `ssh-copy-id` falla con `Permission denied (publickey)` | El paso 1.3 apagó la contraseña por SSH | Otra persona con acceso agrega la llave a `authorized_keys`, o se activa la contraseña un momento desde la consola local (ver `ARRANQUE-LAB.md`, A.1) |
| `/etc/fstab` con dos montajes en `/srv/cdn` | Se agregó la línea del disco USB sin quitar la del archivo de 10 GB; los dos se llaman `HUBDATA` | Dejar una sola línea (`ARRANQUE-LAB.md`, B.4) |
| El portátil no ve la web del AP | El AP solo responde a su red | NAT de laboratorio `lab: portatil a la web del AP`; se borra al cerrar |
| SSH se cuelga tras `ufw enable` | Faltaba la regla del portátil | `sudo ufw allow from 10.42.0.0/24` desde la consola local |
| 18/11: nginx, kiwix y squid caídos al arrancar | `/srv/cdn` sin montar: `fstab` con dos líneas `HUBDATA` (disco USB y `hubdata.img`). El portal y Kiwix estaban solo en `hubdata.img` | Se copiaron `www/` y `kiwix/` al disco USB (`cp -a`), se comentó la línea de `hubdata.img` (queda de respaldo) y se montó `/dev/sdb1` en `/srv/cdn` |
| 18/11: Raspberry con fecha del 30/10 y MikroTik `waiting` en NTP | La Pi no tiene RTC con pila y arrancó sin Internet; chrony no resolvió los pools | `sudo systemctl restart chrony` con Internet. El MikroTik pasó a `synchronized` con 10.20.0.162. Sin la hora correcta, el certificado (emitido el 13/11) aparece como “aún no válido” |
| 18/11: comandos de varias líneas por `ssh` fallan con `bad command name add` | Por SSH no interactivo cada línea se ejecuta sola y pierde el menú (`/ip firewall filter`) | Escribir la ruta completa en cada línea (`/ip firewall filter add ...`). Sin modo seguro, se usó un `/system scheduler` que borraba las reglas `hub:` a los 5 min si se perdía el acceso |
| 18/11: el portátil pierde enlace en `ether9` | Cable o conector flojo | Cambiar el cable; al volver, repetir `ip route replace` |
| 18/11: la Pi aceptaba contraseña por SSH (P2 fallaba) | `10-hub.conf` quedó con `PasswordAuthentication yes` tras usar el plan B de A.1 | `sed` a `no`, `sshd -t` y `systemctl restart ssh`. Después del plan B, cerrar siempre |
| 18/11: SSH a la Pi sin llave del portátil nuevo | `ssh-copy-id` | La Pi aceptó contraseña (`publickey,password`); llave agregada con `ssh-copy-id`. En el MikroTik: `/user ssh-keys import` |

### Siguiente (Fase 3)

- Disco SSD de 2–4 TB definitivo y Squid con 50–100 GB de caché.
- RTC con pila (`dtparam=rtc_bbat_vchg=3000000`) para tener hora sin Internet tras el apagado al 15 %.
- Certificado real con certbot (DNS-01) cuando el profesor confirme el dominio.
- Regenerar la CA de pruebas con `nameConstraints=critical,permitted;DNS:hub.lan`: la actual (`CA:TRUE` sin restricciones) podría firmar certificados para cualquier dominio si se filtra `ca.key`.

## Rúbrica Fase 2 (objetivo *Accomplished*)

- SO optimizado para discos de 2–4 TB y con seguridad básica.
- Caché rápida de sitios populares y archivos educativos, también offline.
- DHCP/DNS local robusto y portal cautivo básico.
