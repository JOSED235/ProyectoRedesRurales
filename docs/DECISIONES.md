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
