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

## Siguiente: 2.2 y servicios

- 2.2: MikroTik físico (`/import hub-base.rsc`) y servicios en el hub: `dnsmasq` (DHCP con relay del MikroTik + DNS), `chrony`, Docker, Nginx, Squid, Mosquitto.
- Firewall entre VLAN, Hotspot (portal cautivo) y colas en el MikroTik.
- Disco 2–4 TB por USB 3, NVMe con HAT, temperatura (`vcgencmd measure_temp`) y consumo.

## Rúbrica Fase 2 (objetivo *Accomplished*)

- SO optimizado para discos de 2–4 TB y con seguridad básica.
- Caché rápida de sitios populares y archivos educativos, también offline.
- DHCP/DNS local robusto y portal cautivo básico.
