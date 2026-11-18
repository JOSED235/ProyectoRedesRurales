# Arranque en el laboratorio — retomar la Fase 2.3

Lista corta para volver a dejar todo como quedó el **17/11/2026** y terminar lo que falta. El detalle de cada paso está en [`Fase2.3_Servicios_AP_Portal_Cautivo.pdf`](Fase2.3_Servicios_AP_Portal_Cautivo.pdf).

**Qué ya funciona (respaldo 17/11):** Raspberry con ufw, SSH solo con llave, disco en `/srv/cdn`, dnsmasq (DNS + DHCP de las 3 VLAN), chrony, Nginx con HTTPS, Kiwix, Squid. MikroTik con relay DHCP, NTP desde la Raspberry, desvío de HTTP a Squid (PBR + netwatch). TP-Link con Hub-Salud (VLAN 20) y Hub-Publica (VLAN 30), DHCP apagado, IP `10.20.0.163`.

**Qué falta:** certificado en el MikroTik, Hotspot, firewall entre VLAN, colas, enlace en `login.html`, pruebas P1–P15 con capturas.

> Las contraseñas **no** están en este repositorio (es público). Pídelas a Carol o al compañero por un canal privado.

---

## A. Antes de ir (en casa)

### A.1 Tu llave SSH en la Raspberry

La Raspberry ya **no acepta contraseña por SSH** (`PasswordAuthentication no`). Por eso `ssh-copy-id` falla con `Permission denied (publickey)`. Tu llave la tiene que agregar alguien que ya entra.

En tu portátil:

```bash
ls ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519     # Enter tres veces
cat ~/.ssh/id_ed25519.pub                             # copia la línea completa
```

Envía esa línea a Carol. Ella, desde su portátil con acceso:

```bash
ssh carol@10.20.0.162 "echo 'ssh-ed25519 AAAA...tu-llave... jose' >> ~/.ssh/authorized_keys"
```

**Plan B (en el lab, si nadie la agregó):** conecta monitor (micro HDMI) y teclado a la Raspberry. Entra como `carol` con su contraseña: la contraseña sí sirve en la consola local. Luego:

```bash
sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config.d/10-hub.conf
sudo systemctl restart ssh
# desde tu portátil:  ssh-copy-id carol@10.20.0.162
# y de vuelta en la Raspberry, cerrar otra vez:
sudo sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config.d/10-hub.conf
sudo systemctl restart ssh
```

### A.2 Archivos en el portátil

Del `respaldo-2026-11-17.zip` (no está en git porque tiene credenciales):

```bash
mkdir -p ~/hub-rural/{mikrotik,servidor,tplink}
unzip respaldo-2026-11-17.zip -d /tmp/respaldo
cp /tmp/respaldo/respaldo-2026-11-17/hub-ccr2004-2026-11-17.backup ~/hub-rural/mikrotik/
cp /tmp/respaldo/respaldo-2026-11-17/configBACKUP.bin ~/hub-rural/tplink/config-hub.bin        # config del hub
cp /tmp/respaldo/respaldo-2026-11-17/config.bin       ~/hub-rural/tplink/config-original.bin   # config del otro grupo
cp /tmp/respaldo/respaldo-2026-11-17/respaldo-hub-2026-11-17.tgz ~/hub-rural/servidor/
git clone https://github.com/JOSED235/ProyectoRedesRurales.git ~/hub-rural/repo
```

| Archivo del zip | Qué es | Comprobado |
|---|---|---|
| `hub-ccr2004-2026-11-17.backup` | Respaldo binario del MikroTik (se carga con `/system backup load`) | — |
| `hub-ccr2004-2026-11-17.rsc` | `/export` en texto; copia en [`configs/mikrotik/`](../configs/mikrotik/hub-ccr2004-2026-11-17.rsc) | Sí |
| `configBACKUP.bin` | TP-Link **del hub**: IP `10.20.0.163`, SSID 1 → VLAN 20, SSID 2 → VLAN 30, DHCP apagado | Sí |
| `config.bin` | TP-Link **original del otro grupo**: IP `10.20.10.3`, VLAN 10/40 | Sí |
| `respaldo-hub-2026-11-17.tgz` | `/etc` de la Raspberry (incluye `ca.key` y `hub.key`: no subir) | Sí |
| `ca-hub.crt` | CA de pruebas para instalar en los celulares (vence 15/02/2029) | Sí |

### A.3 Datos que debes llevar

- [ ] Contraseña de `admin` del MikroTik.
- [ ] Contraseña con la que se guardó `hub-ccr2004-2026-11-17.backup`.
- [ ] Contraseña de `admin` del TP-Link y clave WiFi de Hub-Salud.
- [ ] Contraseña de `carol` en la Raspberry (para `sudo`).
- [ ] Clave para los usuarios de salud del Hotspot (reemplaza `CAMBIAR_CLAVE_SALUD`).

---

## B. En el laboratorio, en este orden

### B.1 Portátil y consola del MikroTik

1. Portátil: WiFi con Internet y la conexión cableada en **IPv4 Compartida con otros equipos**. Cable a `ether9`.
2. Cable de consola USB y:

```bash
ls /dev/ttyUSB*
sudo screen /dev/ttyUSB0 115200
```

### B.2 MikroTik: guardar lo del otro grupo y cargar el hub

El MikroTik es compartido. Primero respalda lo que tiene:

```
/system backup save name=sw01-original-AAAA-MM-DD password=<clave del otro grupo>
```

Sube `hub-ccr2004-2026-11-17.backup` al MikroTik como en la Fase 2.2 (paso E6). Luego:

```
/system backup load name=hub-ccr2004-2026-11-17.backup password=<clave del respaldo>
```

Al reiniciar debe aparecer `[admin@hub-mikrotik] >`.

### B.3 Ruta y acceso desde el portátil

```
/ip dhcp-client print                 # en el MikroTik: IP de ether9 (antes fue 10.42.0.116)
```

```bash
ip -br link                                                     # nombre de tu puerto cableado
sudo ip route replace 10.20.0.0/24 via <IP de ether9> dev <tu-puerto>
ssh admin@10.20.0.161                                           # MikroTik
ssh carol@10.20.0.162                                           # Raspberry
```

La ruta se borra al reiniciar el portátil o desconectar el cable.

### B.4 Raspberry: encender y revisar

Cable a `ether10`, fuente oficial de 27 W, disco USB en un puerto azul (si se usa). En la Raspberry:

```bash
systemctl is-active dnsmasq chrony nginx kiwix squid     # cinco veces "active"
findmnt /srv/cdn                                         # ext4 con noatime
sudo ufw status | head -3                                # Status: active
```

**Revisar el disco.** El `/etc/fstab` del respaldo tiene **dos** líneas que montan `/srv/cdn`: el disco USB (`LABEL=HUBDATA`) y el archivo de 10 GB (`hubdata.img`). Las dos tienen la etiqueta `HUBDATA`. Si el disco USB está conectado, el archivo se monta encima y tapa el disco. Deja solo una línea:

```bash
lsblk -o NAME,SIZE,LABEL,MOUNTPOINT
# Con disco USB: comentar la línea del archivo
sudo sed -i 's|^/var/lib/hub/hubdata.img|#&|' /etc/fstab
# Sin disco USB: comentar la del disco
# sudo sed -i 's|^LABEL=HUBDATA|#&|' /etc/fstab
sudo systemctl daemon-reload && sudo umount -R /srv/cdn; sudo mount -a && findmnt /srv/cdn
```

Si Squid, Nginx o Kiwix no arrancan, casi siempre es que `/srv/cdn` no está montado (`RequiresMountsFor`).

### B.5 TP-Link: guardar lo del otro grupo y cargar el hub

1. Cable del portátil al LAN del TP-Link. Portátil en IPv4 manual `10.20.10.100/24`, sin gateway.
2. Abre `http://10.20.10.3`. Si no responde, búscalo con `sudo tcpdump -i <tu-puerto> -n -e ether host f4:f2:6d:59:80:b6` mientras lo reinicias (PDF, 6.1).
3. **System Tools → Backup & Restore → Backup**: guárdalo como `~/hub-rural/tplink/config-original-AAAA-MM-DD.bin`.
4. **Restore** con `config-hub.bin`. Se reinicia en `10.20.0.163`.
5. Cable del TP-Link a `ether11`. Portátil de vuelta a `ether9` en *Compartida* y repetir la ruta de B.3.
6. En el MikroTik: `/ping 10.20.0.163 count=3`.

### B.6 Prueba rápida de lo que ya estaba

- Celular en **Hub-Publica**: IP entre `10.20.0.10` y `.126`, gateway `10.20.0.1`, DNS `10.20.0.162`.
- Celular en **Hub-Salud**: IP entre `10.20.0.135` y `.158`, gateway `10.20.0.129`.
- Raspberry: `cat /var/lib/misc/dnsmasq.leases` muestra los dos.
- `http://neverssl.com` desde el celular y `sudo tail -n 5 /var/log/squid/access.log` en la Raspberry muestra su IP.

---

## C. Terminar la Fase 2.3

### C.1 Certificado al MikroTik

En la Raspberry:

```bash
sudo install -m 600 -o carol /etc/hub/pki/hub.key ~/hub.key
```

En el portátil:

```bash
cd ~/hub-rural/servidor
scp carol@10.20.0.162:/etc/hub/pki/hub.crt carol@10.20.0.162:hub.key .
ssh carol@10.20.0.162 'rm ~/hub.key'
scp hub.crt hub.key admin@10.20.0.161:
rm hub.key
```

### C.2 Hotspot, firewall y colas

Pega [`configs/mikrotik/fase23-pendiente.rsc`](../configs/mikrotik/fase23-pendiente.rsc) **por bloques**, en orden. Antes del bloque 8.1 presiona `Ctrl+X` (modo seguro).

### C.3 Enlace al contenido en la página del portal

```bash
mkdir -p ~/hub-rural/mikrotik/hotspot && cd ~/hub-rural/mikrotik/hotspot
scp admin@10.20.0.161:hotspot/login.html . && cp login.html login.html.original
nano login.html      # justo después de <body ...> pega la línea de abajo
scp login.html admin@10.20.0.161:hotspot/login.html
```

```html
<p style="text-align:center;font-size:18px"><a href="https://portal.hub.lan">Ver contenido sin conexión</a></p>
```

### C.4 Pruebas P1–P15

Tabla completa en el PDF (sección 9) y en [`README.md`](README.md#23--servicios-access-point-y-portal-cautivo). Una captura por prueba.

---

## D. Al salir

1. **Guardar** (MikroTik, Raspberry, TP-Link): PDF sección 10.1. Sube a `configs/` los archivos de texto nuevos (`.rsc`, configs de `/etc`) y deja los binarios y llaves fuera de git.
2. **Devolver los equipos** (PDF 10.2), en este orden:
   1. TP-Link: **Restore** con `config-original.bin` y desconectarlo de `ether11`.
   2. Raspberry: `ssh -t carol@10.20.0.162 'sudo shutdown -h now'`.
   3. MikroTik: `/ip firewall nat remove [find comment~"lab: portatil a la web del AP"]`, borrar `hub.crt` y los `hub-*` de Files, y por consola `/system backup load name=sw01-original-AAAA-MM-DD.backup password=<clave>`. Debe volver `[admin@sw01] >`.
   4. Desconectar `ether9`, `ether10` y la consola. Portátil cableado en IPv4 Automático.
