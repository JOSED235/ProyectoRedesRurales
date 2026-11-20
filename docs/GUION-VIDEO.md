# Guion del video — Hub rural sin Internet (versión para editar)

**Duración final:** 10 a 12 min. **JD** = José David, **CA** = Carol.

El video se arma en dos partes:

- **Parte A — en el laboratorio, ahora:** solo se graban **clips de pantalla y de los equipos**, cortos y sin hablar (o hablando poco, el audio se reemplaza). Cada clip tiene un código (`C1`, `C2`…) para encontrarlo al editar.
- **Parte B — en casa:** se graba **toda la narración** (teoría y la voz de la demo) como audios separados (`A1`, `A2`…), con calma y buen micrófono.
- **Parte C — montaje:** cada audio va encima de sus clips. Así nunca queda la pantalla quieta mientras se explica: la teoría va sobre tomas de los equipos, diagramas y capturas que ya tenemos.

---

# PARTE A — Grabar en el laboratorio (≈ 30 min)

## Antes de grabar

- [ ] Starlink en `ether9`, Pi en `ether10`, TP-Link en `ether11`, portátil en `ether12` (IP `10.20.0.17x`).
- [ ] WiFi del portátil **apagado**.
- [ ] Celular: olvidar **Hub-Publica** y **Hub-Salud**; activar «No molestar»; brillo alto.
- [ ] Terminal con letra grande (Ctrl + +) y fondo oscuro. Pestañas: `ssh admin@10.20.0.161` (MikroTik) y `ssh carol@10.20.0.162` (Pi). Limpiar con `clear` antes de cada clip.
- [ ] Grabador de pantalla del portátil listo (por ejemplo, GNOME: Ctrl + Alt + Shift + R) y grabación de pantalla del celular.
- [ ] Nunca escribir contraseñas con la grabación encendida: pausar o cortar.

**Regla para todos los clips:** empezar a grabar, esperar 2 s quietos, hacer la acción despacio, esperar 3 s al final y cortar. Si algo sale mal, repetir el clip completo (es más fácil que editar).

## Orden de grabación

El orden está pensado para no cambiar de equipo muchas veces; no es el orden del video.

### Equipos (cámara del celular, horizontal)

| Clip | Qué grabar | Duración |
|---|---|---|
| **C1** | Plano general de la mesa con los cuatro equipos y los cables. Paneo lento de izquierda a derecha. | 10 s |
| **C2** | Starlink Mini (de frente y el cable que sale de ella). | 6 s |
| **C3** | MikroTik CCR2004: luces y los puertos `ether9` a `ether12` con sus cables. Acercarse a cada puerto. | 12 s |
| **C4** | TP-Link: el equipo y el cable que va a `ether11`. | 6 s |
| **C5** | Raspberry Pi 5 con el disco USB. | 6 s |
| **C6** | *(Opcional)* Los dos frente a la mesa saludando y, aparte, despidiéndose (sin audio o diciendo solo «hola» / «gracias»). | 2 × 5 s |

### Celular (grabación de pantalla)

| Clip | Qué hacer en el celular | Duración |
|---|---|---|
| **C7** | App de Starlink mostrando **«Sin señal»** / obstrucciones. | 8 s |
| **C8** | Conectarse a **Hub-Publica** → tocar la red → mostrar detalles: IP `10.20.0.x`, puerta de enlace, DNS `10.20.0.162`. | 20 s |
| **C9** | Navegador → `http://neverssl.com` → aparece la **página de acceso** → quedarse 3 s → tocar «Ver contenido sin conexión» → aparece el portal → bajar despacio por Educación, Salud y Ocio. | 30 s |
| **C10** | En Salud, abrir la **Guía de primeros auxilios** (PDF) y pasar un par de páginas. | 15 s |
| **C11** | Volver al portal → escribir **«energía»** en el buscador → esperar los resultados (portal + Wikipedia, palabra resaltada) → abrir el artículo **«Energía»** y bajar un poco. | 30 s |
| **C12** | *(Opcional, aislamiento)* Desde Hub-Publica abrir `http://10.20.0.163` y dejar ver que no carga (o que vuelve a la página de acceso). | 15 s |
| **C13** | Cambiar a **Hub-Salud** → aparece la página de inicio de sesión de salud. **Pausar**, escribir usuario y clave, **reanudar** → página de estado con el usuario conectado. | 20 s |

### Terminal del portátil (grabación de pantalla)

Grabar justo después de C13, para que la sesión de salud siga activa.

| Clip | Pestaña | Comandos (escribirlos despacio, uno por uno) | Duración |
|---|---|---|---|
| **C14** | MikroTik | `/ip hotspot active print` | 10 s |
| **C15** | MikroTik | `/ip dhcp-client print` · `/ping 192.168.1.1 count=3` · `/ping 8.8.8.8 count=3` | 25 s |
| **C16** | MikroTik | `/queue simple print proplist=name,target,priority,limit-at,max-limit` | 10 s |
| **C17** | MikroTik | `/system ntp client print` | 8 s |
| **C18** | Pi | `systemctl is-active dnsmasq chrony nginx kiwix squid` · `findmnt /srv/cdn` | 15 s |
| **C19** | Pi | `cat /var/lib/misc/dnsmasq.leases` · `chronyc tracking \| head -4` | 15 s |
| **C20** | Navegador del portátil | `https://portal.hub.lan` → bajar hasta el pie con los nombres de los autores. | 15 s |

**Al terminar:** revisar en el celular y en el portátil que estén todos los clips del C1 al C20 antes de desconectar nada. Pasarlos a una carpeta `video/clips/` con su código en el nombre (`C09-portal-acceso.mp4`).

## Si algo falla

- No aparece la página de acceso: abrir `http://neverssl.com`. Si ya había sesión, cerrarla en `wifi-publica.hub.lan/status`.
- Error de certificado: revisar la hora de la Raspberry con `date`.
- El celular no recibe IP: olvidar la red y volver a conectar.
- El buscador no muestra la Wikipedia: en la Raspberry, `systemctl is-active kiwix`.
- No hay acceso al MikroTik: revisar que el portátil esté en `ether12` con IP `10.20.0.17x`.

---

# PARTE B — Narración para grabar en casa

Grabar cada bloque como un archivo aparte (`A1-JD.m4a`, `A2-JD.m4a`…), en un cuarto silencioso, con el celular a un palmo de la boca. Dejar 2 s de silencio al inicio y al final. Si te equivocas, repite la frase completa sin parar la grabación; se corta al editar.

Entre corchetes está el clip o la imagen que irá encima.

### A1 — Presentación (JD, 45 s)

> [C6 o C1]
> Hola, profesor. Somos José David Rodríguez y Carol Mosquera, del curso Infraestructura de Redes 2. En este video le mostramos el hub rural que construimos: una red local para una unidad de atención comunitaria en una zona rural. Da Internet satelital cuando hay señal y, cuando no la hay, sigue ofreciendo lo importante: conexión WiFi, acceso por grupos, contenido educativo y de salud, y una Wikipedia sin conexión.
>
> [C7 — app de Starlink sin señal]
> Todo lo que van a ver funciona sin Internet. La antena Starlink está conectada, pero dentro del laboratorio no ve el cielo, así que no hay salida a Internet. Es justo lo que pasaría en el sitio un día nublado o si se cae el enlace.

### A2 — Los equipos (JD, 2 min)

> [C1] La arquitectura tiene cuatro piezas.
>
> [C2] La primera es la Starlink Mini, el enlace a Internet. Va por cable al puerto ether9 del enrutador, que es nuestra WAN. El enrutador recibe su dirección por DHCP, así que da igual si la WAN es la Starlink o, como hicimos en el laboratorio para descargar cosas, el portátil compartiendo su WiFi.
>
> [C3] La segunda es el enrutador MikroTik CCR2004, con RouterOS 7. Es el centro de la red. Funciona en modo router-on-a-stick: un solo bridge con tres redes virtuales separadas, que salen del bloque 10.20.0.0/24 dividido con VLSM.
> [diagrama de topología `docs/img/f1-carol-topologia.png` o tabla de VLAN]
> La VLAN 10, de administración, tiene el enrutador, el servidor y el punto de acceso; solo desde aquí se administran los equipos. La VLAN 20 es la de salud, para el personal del puesto. Y la VLAN 30 es la pública, para la comunidad, hasta unos 120 dispositivos.
> [`docs/img/f22-puertos-ccr2004.png`]
> El MikroTik además hace el NAT hacia Internet, el portal cautivo de cada grupo, el firewall que aísla las VLAN, el control de ancho de banda y el desvío del tráfico web hacia la caché.
>
> [C4] La tercera pieza es el punto de acceso TP-Link, conectado a ether11 por un troncal 802.1Q. Emite dos redes WiFi: Hub-Salud, que va a la VLAN 20, y Hub-Publica, que va a la VLAN 30. Así cada persona queda en su red según el WiFi al que se conecte.
>
> [C5] La cuarta es el servidor, una Raspberry Pi 5 con Ubuntu Server 24.04, en ether10 con la dirección 10.20.0.162, y un disco USB donde está todo el contenido. Carol les explica sus servicios.

### A3 — Servicios del servidor (CA, 1 min 30 s)

> [C18 — se ven los cinco «active»]
> Gracias, José. En la Raspberry corren cinco servicios, y aquí ven que los cinco están activos.
>
> [C5 o C18 congelado]
> dnsmasq es el DNS y el DHCP de las tres VLAN. El MikroTik le reenvía las solicitudes con un relay, así que un solo servidor reparte las direcciones de toda la red. También resuelve nuestros nombres locales, como portal.hub.lan o wiki.hub.lan, aunque no haya Internet.
> chrony da la hora a toda la red, y el MikroTik se sincroniza con la Raspberry. Es importante porque sin la hora correcta el HTTPS falla.
> Nginx es el servidor web: publica el portal, los PDF y las páginas guardadas, todo por HTTPS con nuestro propio certificado.
> Kiwix sirve la Wikipedia en español sin conexión.
> Y Squid es la caché web. Cuando hay Internet guarda lo que la gente descarga, para que la segunda persona que lo pide no gaste otra vez el enlace satelital.
>
> [final de C18 — `findmnt`]
> El contenido está en un disco USB montado en /srv/cdn con la opción noatime, para no desgastarlo escribiendo en cada lectura. La Raspberry también tiene firewall y SSH solo con llave.

### A4 — No hay Internet (CA, 50 s)

> [C7] Antes de la demo comprobemos que de verdad no hay Internet. En la app, la Starlink aparece sin señal.
>
> [C15] En el MikroTik, el puerto WAN recibió la dirección 192.168.1.159 de la Starlink, y su router responde. O sea, el equipo está bien integrado: el cable, el DHCP y el enlace funcionan. Pero el ping a 8.8.8.8, un servidor de Google, no responde. No hay salida a Internet. Desde aquí, todo lo que hagamos con el celular sale del propio hub.

### A5 — Usuario de la comunidad (JD, 1 min 45 s)

> [C8] Ahora soy una persona de la comunidad y me conecto al WiFi Hub-Publica. El celular recibió una dirección de la VLAN pública. Se la entregó la Raspberry a través del relay del MikroTik, aunque no haya Internet.
>
> [C9, hasta la página de acceso] Al abrir cualquier página aparece el portal cautivo, la página de acceso del hub. En la red pública hay dos opciones: navegar en Internet gratis por dos horas al día, que ahora no serviría porque no hay señal, y ver el contenido sin conexión, que no pide iniciar sesión.
>
> [C9, portal] Este es el portal del hub. Está organizado en tres categorías: Educación, Salud y Ocio. Arriba dice cuántos documentos hay, y todo carga al instante porque está en el servidor del puesto.
>
> [C10] Por ejemplo, en Salud están las guías de lavado de manos y de primeros auxilios, basadas en la OMS y la Cruz Roja. Se abren directamente en el celular.

### A6 — Wikipedia sin conexión (CA, 50 s)

> [C11, escribiendo] El buscador revisa primero lo que hay en el portal y, al mismo tiempo, busca en la Wikipedia sin conexión. Los resultados aparecen aquí mismo, con la palabra resaltada.
>
> [C11, artículo] Al tocar un resultado se abre el artículo completo, servido por Kiwix desde la Raspberry. Para la demo cargamos la parte de física de la Wikipedia en español; en la versión final se carga una colección más grande en el disco del hub.

### A7 — Personal de salud y aislamiento (CA, 1 min 30 s)

> [C13] Ahora soy del personal de salud. Me conecto a Hub-Salud, que está en otra VLAN, la 20. Aquí no hay prueba gratis: se entra con usuario y contraseña, porque es la red del puesto.
>
> [C14] Ya inicié sesión, y en el MikroTik aparece la sesión activa con su usuario y su dirección.
>
> [C12, o diagrama de VLAN] Las dos redes están aisladas. Desde la red pública no se llega ni a la red de salud ni a los equipos de administración: el firewall bloquea el tráfico entre VLAN y solo deja pasar lo necesario, como el DNS, la hora y el contenido del servidor.
>
> [C16] El ancho de banda también está repartido por prioridad. Salud tiene 3 megabits de subida y 10 de bajada garantizados, con prioridad alta. La red pública tiene un máximo de 5 y 20 para todo el grupo, y de 1 y 2 megabits por persona. Así nadie acapara el enlace satelital.

### A8 — Lo que pasa por dentro (JD, 1 min 30 s)

> [C19, concesiones] Por dentro, esto es lo que acaba de pasar. Aquí están las concesiones del DHCP: el celular y el portátil, cada uno en su VLAN.
>
> [C19, chrony → C17] La hora se mantiene aunque no haya Internet, y el MikroTik sigue sincronizado con la Raspberry.
>
> [`docs/img/f23-p12-squid-hit.png`] Cuando sí hay Internet, el tráfico web de los usuarios pasa de forma transparente por la caché Squid. Lo probamos en el laboratorio: la primera descarga de un archivo tardó medio segundo y la segunda, que salió de la caché, dos milésimas.
> [`docs/img/f23-p13-pbr-desactivado.png` → `f23-p13-pbr-reactivado.png`] Si Squid se cae, el MikroTik lo detecta en diez segundos y deja de enviarle tráfico, así que los usuarios siguen navegando. El HTTPS no se intercepta, para no exponer datos de salud.

### A9 — Cierre (CA + JD, 45 s)

> [C20] **CA:** En resumen: con la Starlink sin señal, el hub siguió entregando direcciones, resolviendo nombres, dando la hora, mostrando el portal cautivo por grupo y sirviendo los documentos, la Wikipedia y los cursos guardados. Eso es un diseño offline first: Internet suma, pero no es indispensable.
>
> [C1 o C6] **CA:** Lo que sigue, en la Fase 3, es un disco más grande para la caché y el contenido, video con Jellyfin, sincronizar el contenido cada vez que vuelva la conexión, una pila para la hora sin Internet y medir el consumo de energía.
>
> **JD:** Gracias por su atención, profesor.

---

# PARTE C — Montaje

| Min. aprox. | Audio | Imagen encima |
|---|---|---|
| 0:00 | A1 | C6/C1 → C7 |
| 0:45 | A2 | C1 → C2 → C3 → topología → puertos → C4 → C5 |
| 2:45 | A3 | C18 (ralentizado o congelado mientras explica cada servicio) |
| 4:15 | A4 | C7 → C15 |
| 5:05 | A5 | C8 → C9 → C10 |
| 6:50 | A6 | C11 |
| 7:40 | A7 | C13 → C14 → C12/diagrama → C16 |
| 9:10 | A8 | C19 → C17 → capturas de Squid y PBR |
| 10:40 | A9 | C20 → C1/C6 |

Consejos:

- Si un clip es más corto que su audio, **congelar el último cuadro** o ponerlo a 0,7×; si es más largo, cortar las esperas o acelerarlo (la escritura de comandos a 2× se ve bien).
- En los comandos, hacer **zoom** al resultado importante (los cinco `active`, el `100% packet-loss` del ping a 8.8.8.8, la sesión en `hotspot active`).
- Rótulos cortos abajo al cambiar de escena: «Sin Internet», «Red pública — VLAN 30», «Red de salud — VLAN 20».
- Editor sugerido: CapCut o DaVinci Resolve (gratis). Exportar en 1080p.
