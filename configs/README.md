# Configuraciones de los equipos

Archivos que se copian tal cual a los equipos. Se prueban primero en el laboratorio GNS3 y luego se llevan al hardware físico.

| Archivo | Equipo | Dónde se aplica | Cómo |
|---|---|---|---|
| [`mikrotik/hub-base.rsc`](mikrotik/hub-base.rsc) | MikroTik (RouterOS 7) | CHR en GNS3 y MikroTik físico | Pegar por consola, o subirlo por WinBox (Files) y ejecutar `/import hub-base.rsc` |
| [`servidor/01-hub.yaml`](servidor/01-hub.yaml) | Hub Raspberry Pi 5 (Ubuntu Server 24.04) | `/etc/netplan/01-hub.yaml` | Deshabilitar la red de cloud-init, luego `sudo netplan generate && sudo netplan apply` |

## Reglas

- Después de cada cambio en el MikroTik, ejecutar `/export` y reemplazar `hub-base.rsc` con esa salida.
- En el MikroTik físico, revisar los nombres de puertos del modelo antes de importar. El físico se resetea con `/system reset-configuration no-defaults=yes skip-backup=yes`.
- En la VM de GNS3 la interfaz del servidor es `ens3`; en la Raspberry Pi es `eth0`.
- No subir las reglas propias del laboratorio al equipo físico. Ejemplo: aceptar gestión desde `192.168.122.1`.
- No guardar contraseñas ni claves en estos archivos.

## Pendiente (Fase 2)

- Firewall entre VLAN, Hotspot (portal cautivo), colas y relay DHCP en el MikroTik.
- Configuraciones del hub: `dnsmasq`, `chrony`, Squid, Nginx, `docker-compose.yml`.
