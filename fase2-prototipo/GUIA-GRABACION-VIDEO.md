# Guía para terminar la grabación del video en el laboratorio

Para: Carol. Tiempo estimado: **1 hora** (15 min de montaje y comprobación + 30 min de clips + 15 min de cierre).
Guion completo y narraciones: [`docs/GUION-VIDEO.md`](../docs/GUION-VIDEO.md). Aquí solo se graban **clips sin hablar**; la voz se graba después en casa.

---

## 0. Qué llevar

- Portátil con cable de red (o adaptador USB-Ethernet) y el repositorio actualizado (`git pull`).
- Celular con batería y espacio (≈ 2 GB), con la grabación de pantalla activada.
- Datos de acceso (pedírselos a José David, **no** están en el repo): clave de `admin` del MikroTik, clave de tu usuario `carol` en la Pi y usuario/clave de salud (`enfermera01`).

## 1. Montaje físico

Si los equipos ya están conectados y encendidos, salta al paso 2.

| Cable | Desde | Hasta el MikroTik |
|---|---|---|
| Starlink Mini (cable de datos de la Mini) | Starlink | `ether9` |
| Raspberry Pi 5 | Puerto Ethernet de la Pi | `ether10` |
| TP-Link | Puerto LAN/PoE del TP-Link | `ether11` |
| Portátil | Tu puerto de red | `ether12` |

Encender en este orden y esperar:

1. **MikroTik** → esperar ~2 min hasta que dejen de parpadear rápido las luces.
2. **Raspberry Pi** (con el disco USB conectado **antes** de encender) → esperar ~1 min.
3. **TP-Link** → esperar ~1 min hasta que aparezcan las redes Hub-Salud y Hub-Publica.
4. **Starlink Mini** → abrir la app de Starlink en el celular; debe mostrar **«Sin señal»** u obstrucciones (es lo que queremos).

## 2. Conectar el portátil sin perder Internet

El cable del hub no tiene Internet. Si Linux lo usa como ruta principal, el portátil se queda sin Internet. Para evitarlo, en Linux (una sola vez):

```bash
nmcli con show                       # ver el nombre de la conexión cableada, p. ej. "Conexión cableada 1"
nmcli con mod "Conexión cableada 1" \
  ipv4.never-default yes ipv6.never-default yes \
  ipv4.ignore-auto-dns yes ipv4.dns 10.20.0.162 ipv4.dns-search "~hub.lan" \
  ipv4.routes "10.20.0.0/24 10.20.0.161"
nmcli con up "Conexión cableada 1"
```

> En Windows o Mac no hace falta nada: conecta el cable y listo (si pierdes Internet, da igual para grabar).

Comprobar:

```bash
ip -4 -br addr        # el cable debe tener 10.20.0.17x/28
ping -c2 10.20.0.161  # MikroTik responde
ping -c2 10.20.0.162  # Raspberry responde
```

**Si no aparece la IP `10.20.0.17x`:** desconectar y volver a conectar el cable; revisar que esté en `ether12`.

## 3. Comprobar que todo funciona (antes de grabar)

Abrir **dos pestañas** de terminal:

- Pestaña 1: `ssh admin@10.20.0.161` (MikroTik)
- Pestaña 2: `ssh carol@10.20.0.162` (Raspberry)

### En la Raspberry (pestaña 2)

```bash
systemctl is-active dnsmasq chrony nginx kiwix squid
findmnt /srv/cdn
date
```

Debe salir: cinco veces `active`; `/dev/sda1 … noatime`; y la **fecha y hora correctas de hoy**.

- **Si algún servicio no está `active`:** casi siempre es que el disco no está montado. `sudo mount -a`, y luego `sudo systemctl restart nginx kiwix squid`.
- **Si la fecha está mal** (la Pi no tiene pila y arrancó sin Internet): `sudo date -s "AAAA-MM-DD HH:MM"` con la hora real, y luego `sudo systemctl restart chrony`. Sin esto, el celular mostrará error de certificado.

### En el MikroTik (pestaña 1)

```
/ip dhcp-client print
/ping 8.8.8.8 count=3
/system ntp client print
```

Debe salir: `ether9 … bound 192.168.1.x`; el ping a 8.8.8.8 con `timeout` (no hay Internet, correcto); NTP `synchronized` con `10.20.0.162`.

- **Si NTP dice `waiting`:** esperar 1–2 min después de arreglar la hora de la Pi.

### En el navegador del portátil

Abrir `https://portal.hub.lan` → debe cargar el portal con las categorías Educación, Salud y Ocio.

Si todo esto sale bien, **el hub está listo**.

## 4. Preparar la grabación

**Celular**

- Ajustes → WiFi → **olvidar** Hub-Publica y Hub-Salud (para que salga la página de acceso desde cero).
- Activar «No molestar» y subir el brillo.
- Probar la grabación de pantalla 5 s y borrar la prueba.

**Portátil**

- Terminal con fondo oscuro y letra grande (**Ctrl + +** tres o cuatro veces).
- Grabador de pantalla listo (Ubuntu: **Ctrl + Alt + Shift + R** para empezar y terminar; Windows: **Win + Alt + R**).
- Escribir `clear` antes de cada clip.

**Reglas para cada clip**

1. Empezar a grabar y quedarse quieta **2 segundos**.
2. Hacer la acción **despacio**.
3. Quedarse quieta **3 segundos** al final y cortar.
4. Si algo sale mal, **repetir el clip completo**.
5. **Nunca** escribir contraseñas con la grabación encendida.
6. No hace falta hablar; el audio se reemplaza.

## 5. Clips que hay que grabar

Marca cada uno al terminarlo. Si José David ya grabó alguno, pregúntale cuáles y sáltalos.

### A. Equipos (cámara del celular, en horizontal)

- [ ] **C1** (10 s) Plano general de la mesa con los cuatro equipos y los cables. Mover la cámara despacio de izquierda a derecha.
- [ ] **C2** (6 s) Starlink Mini de frente y el cable que sale de ella.
- [ ] **C3** (12 s) MikroTik: las luces y los puertos `ether9`, `ether10`, `ether11` y `ether12` con sus cables. Acercarse a cada uno.
- [ ] **C4** (6 s) TP-Link y el cable que va a `ether11`.
- [ ] **C5** (6 s) Raspberry Pi con el disco USB.
- [ ] **C6** (opcional, 2 × 5 s) José David y tú saludando frente a la mesa, y aparte despidiéndose.

### B. Celular (grabación de pantalla)

- [ ] **C7** (8 s) App de Starlink mostrando **«Sin señal»**.
- [ ] **C8** (20 s) Conectarse a **Hub-Publica**. Luego tocar la red conectada → detalles: que se vea la IP `10.20.0.x`, la puerta de enlace `10.20.0.1` y el DNS `10.20.0.162`.
- [ ] **C9** (30 s) Abrir el navegador → escribir `http://neverssl.com` → aparece la **página de acceso del hub** (quedarse 3 s) → tocar **«Ver contenido sin conexión»** → aparece el portal → bajar despacio por Educación, Salud y Ocio.
- [ ] **C10** (15 s) En **Salud**, abrir la **Guía de primeros auxilios** (PDF) y pasar un par de páginas.
- [ ] **C11** (30 s) Volver al portal → escribir **«energía»** en el buscador → esperar los resultados (del portal y de la Wikipedia, con la palabra resaltada) → abrir el artículo **«Energía»** y bajar un poco.
- [ ] **C12** (opcional, 15 s) Abrir `http://10.20.0.163` → no carga o vuelve a la página de acceso (muestra que desde la red pública no se llega a los equipos de administración).
- [ ] **C13** (20 s) WiFi → cambiar a **Hub-Salud** → aparece la página de inicio de sesión de salud → **pausar la grabación** → escribir usuario y clave → **reanudar** → mostrar la página de estado con el usuario conectado.

### C. Terminal del portátil (grabación de pantalla)

Grabar **justo después de C13**, para que la sesión de salud siga activa. Escribir cada comando despacio.

- [ ] **C14** — MikroTik:
  ```
  /ip hotspot active print
  ```
  Debe aparecer la sesión de `enfermera01` con su IP.
- [ ] **C15** — MikroTik:
  ```
  /ip dhcp-client print
  /ping 192.168.1.1 count=3
  /ping 8.8.8.8 count=3
  ```
  El router de la Starlink responde; Google no (`100% packet-loss`).
- [ ] **C16** — MikroTik:
  ```
  /queue simple print proplist=name,target,priority,limit-at,max-limit
  ```
- [ ] **C17** — MikroTik:
  ```
  /system ntp client print
  ```
- [ ] **C18** — Raspberry:
  ```
  systemctl is-active dnsmasq chrony nginx kiwix squid
  findmnt /srv/cdn
  ```
- [ ] **C19** — Raspberry:
  ```
  cat /var/lib/misc/dnsmasq.leases
  chronyc tracking | head -4
  ```
  Deben aparecer el celular y el portátil en las concesiones.
- [ ] **C20** — Navegador del portátil: abrir `https://portal.hub.lan` y bajar despacio hasta el pie, donde están los nombres de los autores.

## 6. Si algo falla durante la grabación

| Problema | Solución |
|---|---|
| No aparece la página de acceso en C9 | Abrir `http://neverssl.com` (con **http**, no https). Si ya había sesión, cerrarla en `wifi-publica.hub.lan/status`. |
| Error de certificado en el celular | La hora de la Pi está mal: ver el paso 3 (`date`). |
| El celular no recibe IP | Olvidar la red y volver a conectar. |
| El buscador no muestra resultados de la Wikipedia | En la Pi: `systemctl is-active kiwix`; si no está activo, `sudo systemctl restart kiwix`. |
| No entra a Hub-Salud | Revisar usuario y clave con José David; probar `enfermera01` o `promotor01`. |
| `hotspot active print` sale vacío en C14 | La sesión de salud se cerró: repetir C13 y grabar C14 enseguida. |
| No hay acceso al MikroTik ni a la Pi | Revisar que el portátil esté en `ether12` y tenga IP `10.20.0.17x`. |

## 7. Al terminar

1. **Revisar** en el celular y en el portátil que estén todos los clips marcados, antes de desconectar nada.
2. **Renombrar** cada archivo con su código: `C09-portal-acceso.mp4`, `C15-ping-sin-internet.mp4`, etc.
3. **Subirlos** a la carpeta compartida del video (Drive) en una carpeta `clips/`.
4. **Cerrar la sesión de salud** en el celular (página de estado → Cerrar sesión).
5. **Apagar** (solo si José David lo indica; si los equipos se quedan para la otra sesión, dejarlos encendidos):
   - Raspberry: en la pestaña 2, `sudo poweroff` y esperar a que la luz verde deje de parpadear antes de desconectarla.
   - MikroTik: en la pestaña 1, `/system shutdown` y confirmar con `y`.
   - Luego desconectar la Starlink y el TP-Link.
6. **No borrar ni cambiar** la configuración del MikroTik: la devolución de equipos la hace José David con el respaldo del otro grupo.
7. Avisar a José David qué clips quedaron y si algo falló.

## 8. Después: narración en casa

Cada uno graba sus bloques de voz (A1 a A9) siguiendo [`docs/GUION-VIDEO.md`](../docs/GUION-VIDEO.md), parte B. A Carol le tocan **A3, A4, A6, A7 y A9** (la primera parte del cierre). Grabar cada bloque como archivo aparte (`A3-CA.m4a`), en un cuarto silencioso, con el celular a un palmo de la boca y 2 s de silencio al inicio y al final.
