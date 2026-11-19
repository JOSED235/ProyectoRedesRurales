# Configuraciones de los equipos

Archivos que se copian tal cual a los equipos. Se probaron primero en el laboratorio GNS3 y luego en el hardware físico.

## MikroTik

| Archivo | Qué es | Cómo se usa |
|---|---|---|
| [`mikrotik/hub-base.rsc`](mikrotik/hub-base.rsc) | Base del laboratorio GNS3 (CHR 7.25, puertos `ether1`–`ether5`) | `/import hub-base.rsc` en un CHR |
| [`mikrotik/hub-ccr2004-2026-11-17.rsc`](mikrotik/hub-ccr2004-2026-11-17.rsc) | `/export` real del CCR2004 del laboratorio (Fase 2.3 hasta el paso 6) | Referencia. En el lab se restaura con el `.backup`, que no se versiona |
| [`mikrotik/hub-ccr2004-2026-11-18.rsc`](mikrotik/hub-ccr2004-2026-11-18.rsc) | `/export` real del CCR2004 con los pasos 7 y 8 (Hotspot, firewall, colas) | Referencia. Sin contraseñas (RouterOS 7 las oculta) |
| [`mikrotik/hotspot/`](mikrotik/hotspot/) | Páginas del Hotspot en español con el estilo del portal: `login.html` (Hub-Publica con prueba gratis, Hub-Salud con usuario y clave), `alogin.html`, `status.html`, `logout.html`, `error.html`, `errors.txt` y `hub.css` | `scp -O hub.css login.html alogin.html status.html logout.html error.html errors.txt admin@10.20.0.161:hotspot/` |
| [`mikrotik/fase23-pendiente.rsc`](mikrotik/fase23-pendiente.rsc) | Certificado, Hotspot, firewall y colas (pasos 7 y 8) | Pegar por bloques sobre el respaldo del 17/11 |

## Servidor hub (Raspberry Pi 5, Ubuntu Server 24.04)

Las rutas dentro de `servidor/etc/` son las mismas de `/etc` en la Raspberry. Copia real del respaldo del 17/11/2026.

| Archivo | Destino | Servicio |
|---|---|---|
| [`servidor/01-hub.yaml`](servidor/01-hub.yaml) | `/etc/netplan/01-hub.yaml` | Red: `10.20.0.162/28`, gw `10.20.0.161` |
| [`servidor/etc/dnsmasq.d/hub.conf`](servidor/etc/dnsmasq.d/hub.conf) | `/etc/dnsmasq.d/hub.conf` | DNS `hub.lan` y DHCP de las VLAN 10/20/30 |
| [`servidor/etc/chrony/conf.d/hub.conf`](servidor/etc/chrony/conf.d/hub.conf) | `/etc/chrony/conf.d/hub.conf` | NTP para la red, también sin Internet |
| [`servidor/etc/ssh/sshd_config.d/10-hub.conf`](servidor/etc/ssh/sshd_config.d/10-hub.conf) | `/etc/ssh/sshd_config.d/10-hub.conf` | SSH solo con llave, solo `carol` |
| [`servidor/etc/nginx/sites-available/hub`](servidor/etc/nginx/sites-available/hub) | `/etc/nginx/sites-available/hub` | Portal, CDN y Kiwix por HTTPS |
| [`servidor/etc/squid/squid.conf`](servidor/etc/squid/squid.conf) | `/etc/squid/squid.conf` | Caché HTTP transparente (`3129 intercept`) |
| [`servidor/etc/systemd/system/kiwix.service`](servidor/etc/systemd/system/kiwix.service) | `/etc/systemd/system/kiwix.service` | Wikipedia sin conexión en `127.0.0.1:8080` |
| [`servidor/etc/systemd/system/squid.service.d/10-disco.conf`](servidor/etc/systemd/system/squid.service.d/10-disco.conf) | `/etc/systemd/system/{nginx,squid,kiwix}.service.d/10-disco.conf` | No arrancar sin `/srv/cdn` montado |
| [`servidor/www/ca-hub.crt`](servidor/www/ca-hub.crt) | `/srv/cdn/www/ca-hub.crt` | CA de pruebas (pública) para los celulares |
| [`servidor/www/index.html`](servidor/www/index.html) | `/srv/cdn/www/index.html` | Portal: categorías Educación/Salud/Ocio y búsqueda local. Lista los documentos de `/srv/cdn/www/pdf/{educacion,salud,ocio}/`; los PDF sueltos en `pdf/` salen en Educación |
| [`servidor/www/certificado.html`](servidor/www/certificado.html) | `/srv/cdn/www/certificado.html` | Guía para instalar la CA en Android, iPhone y PC. Nginx la sirve también por HTTP |

Además, en la Raspberry (no versionado como archivo propio):

- `/etc/fstab`: `LABEL=HUBDATA /srv/cdn ext4 noatime,nofail,x-systemd.device-timeout=10s 0 2` (una sola línea para `/srv/cdn`).
- `/etc/ufw/before.rules`, al inicio: `*nat` con `-A PREROUTING -i eth0 -p tcp --dport 80 ! -d 10.20.0.162 -j REDIRECT --to-ports 3129`.
- Reglas de ufw: paso 1.2 del PDF de la Fase 2.3.

Los servicios se instalan con `apt` y corren con systemd. No se usa Docker en la Fase 2.

## Reglas

- Después de cada cambio en el MikroTik, ejecutar `/export` y guardar la salida aquí con la fecha en el nombre.
- En el MikroTik físico, revisar los nombres de puertos del modelo antes de importar. El físico se resetea con `/system reset-configuration no-defaults=yes skip-backup=yes`.
- En la VM de GNS3 la interfaz del servidor es `ens3`; en la Raspberry Pi es `eth0`.
- No subir las reglas propias del laboratorio al equipo final. Ejemplos: gestión desde `192.168.122.1` o `10.42.0.0/24`, y el NAT `lab: portatil a la web del AP`.
- **El repositorio es público.** No guardar contraseñas, llaves privadas (`ca.key`, `hub.key`) ni respaldos binarios (`.backup`, `.bin` del TP-Link, `.tgz` de `/etc`). El `.gitignore` los excluye.
