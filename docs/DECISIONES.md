# Registro de decisiones y datos importantes

**Regla del equipo (personas y asistentes de IA):** cada vez que se tome una decisión, se cambie una anterior o aparezca un dato que importe para el proyecto (una IP, un puerto, una versión, una fecha, un resultado de prueba, un equipo prestado, un problema y su causa), se anota aquí **en el mismo momento**, con la fecha y el porqué. Después se actualizan el README o el archivo que corresponda y, si aplica, el informe.

Si no está escrito, se pierde: así ya pasó con la fecha de la Fase 2.1, que hubo que sacar de las capturas.

- Nunca anotar contraseñas, llaves privadas ni respaldos: el repositorio es público. Escribir solo dónde están guardadas.
- Una decisión que cambia otra no borra la anterior: se agrega una fila nueva que diga cuál reemplaza.
- Los datos van con su fuente (export, captura, comando, PDF) para poder comprobarlos.

| Fecha | Decisión o dato | Por qué | Dónde quedó |
|---|---|---|---|
| 2026-10-20 | Diseño consolidado: MikroTik + RPi5 + Starlink Mini + UniFi, bloque `10.20.0.0/24`, VLAN 10/20/30 | Une las dos versiones de la Fase 1; separar router y servidor evita que una falla del servidor tumbe la red | `fase1-plan/README.md` |
| 2026-10-26 | Laboratorio GNS3 en Ubuntu, no en Windows | KVM directo, sin virtualización anidada | `fase1-plan/laboratorio-gns3/` |
| 2026-10-30 | Fase 2.1 hecha: RPi5 física por nodo Cloud; puerto del portátil sin IP | Evitar un segundo DHCP y gateway en la VLAN 10 | `fase2-prototipo/README.md` |
| 2026-11-05 | CCR2004 prestado con puertos `ether9`–`ether12`; respaldar y restaurar al otro grupo en cada sesión | No mover los cables del otro grupo | `fase2-prototipo/README.md` |
| 2026-11-13 | Servicios del hub con `apt` + systemd, sin Docker en la Fase 2 | Menos RAM y `RequiresMountsFor=/srv/cdn` | `fase2-prototipo/README.md` |
| 2026-11-13 | AP de laboratorio: TP-Link TL-WA801ND en `10.20.0.163`; el UniFi sigue en el diseño final | Es el AP disponible; misma configuración SSID↔VLAN | `fase2-prototipo/README.md` |
| 2026-11-13 | HTTPS no se descifra en Squid | No exponer datos de salud ni instalar certificados falsos | `configs/servidor/etc/squid/squid.conf` |
| 2026-11-18 | Firewall de 18 reglas `hub:` y colas `salud`/`publica` aplicadas; 11 de 15 pruebas OK | Pasos 7 y 8 de la Fase 2.3 | `configs/mikrotik/hub-ccr2004-2026-11-18.rsc`, `fase2-prototipo/SESION-2026-11-18.md` |
| 2026-11-19 | Informes en `.tex` IEEEtran dentro de `docs/`, compilados con `texlive/texlive:latest-full`, con capturas en `docs/img/` | Formato de entrega del curso | `docs/InformeAvance.tex` |
| 2026-11-19 | Pendiente: cambiar las claves de Hotspot y de respaldos que aparecen en los PDF de las fases 2.2 y 2.3 | Esos PDF están en el repositorio público | — |
| 2026-11-19 | Starlink Mini en modo normal (sin bypass) en `ether9`; la WAN con Internet se simula con el portátil en la misma interfaz | En el lab no hay vista al cielo y el bypass solo se deshace con reinicio de fábrica | `fase2-prototipo/SESION-2026-11-19.md` |
| 2026-11-19 | Portal con fuentes alojadas en el hub (Bricolage Grotesque y Atkinson Hyperlegible, OFL) y búsqueda de Kiwix dentro del portal | Funciona sin Internet; Atkinson mejora la lectura con baja visión; Kiwix sirve XML con CORS abierto | `configs/servidor/www/index.html` |
| 2026-11-19 | Starlink Mini integrada físicamente; sin vista al cielo sirvió como prueba real sin conexión (P11) | Caso real del sitio sin señal | `fase2-prototipo/SESION-2026-11-19.md` |
| 2026-11-20 | CDN de video con Nginx y MP4 720p ≤ 1,2 Mbps con `faststart`, sin Jellyfin | La RPi5 no tiene codificador H.264 por hardware; codificar una vez y servir estático no carga la CPU y cabe en la cola de 2 Mbps | `fase2-prototipo/README.md` (2.4), `configs/servidor/etc/nginx/sites-available/hub` |
| 2026-11-20 | P1, P10 y V1–V4 cumplidas: 15/15 pruebas de red y 4/4 de video | Cierre de la Fase 2 | `docs/InformeFinal.pdf`, Tabla VII |
| 2026-11-23 | Informe final en `docs/InformeFinal.tex` (reconstruido del PDF del 20/11 y del informe de avance), con tabla de rúbrica de las tres fases | La fuente del PDF del 20/11 no estaba en el repositorio; las tablas quedaban después de las referencias | `docs/InformeFinal.pdf` |
