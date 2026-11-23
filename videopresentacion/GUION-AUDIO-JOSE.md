# Guion de audio — José David (complemento del video de Carol)

Se graban **5 audios separados**. Claude arma las diapositivas (diagramas y capturas del informe), las sincroniza con la voz y las inserta en el video. El texto entre corchetes es lo que se verá en pantalla: **no se lee**.

## Cómo grabar

- Grabadora de voz del celular, en un cuarto sin eco ni ruido (sin ventilador). Celular a un palmo de la boca, un poco de lado.
- Cada audio en un archivo: `A1.m4a`, `A2.m4a`, … Guárdalos en `videopresentacion/audios/`.
- Antes de hablar, 2 s en silencio; al terminar, otros 2 s.
- Ritmo tranquilo y natural; no tiene que ser idéntico al texto. Si te equivocas, haz una pausa y repite la frase completa: los errores los corto yo.
- Duración total ≈ 4 min. El video final quedaría en ≈ 13 min.

---

## A1 — Presentación (al inicio, antes de Carol) · ≈ 30 s

[Portada: título del proyecto, nombres, curso, profesor]

> Buenos días, profesor. Somos José David Rodríguez y Carol Mosquera, de Infraestructura de Redes 2. Este video presenta la red local autónoma que diseñamos para una unidad móvil de atención comunitaria en zonas rurales, donde el Internet es escaso y la energía inestable.
>
> Primero Carol muestra los equipos y el sistema funcionando en el laboratorio. Después explicamos cómo llegamos a este diseño, cómo funciona por dentro y cuáles fueron los resultados de las pruebas.

---

## A2 — De dónde salió el diseño (después de la demo de Carol, ≈ 5:15) · ≈ 75 s

[Dos columnas: versión José / versión Carol → diseño consolidado]

> Antes de comprar o montar equipos, cada uno hizo su propia propuesta. La mía usaba la Raspberry Pi como único equipo: enrutador, portal y caché. La de Carol usaba una Mini PC como enrutador, con cuatro VLAN calculadas con VLSM y una matriz de tráfico entre ellas.
>
> Al compararlas decidimos separar funciones: el MikroTik se encarga de la red, es decir, las VLAN, el NAT, el portal cautivo, el firewall y las colas; y la Raspberry se encarga solo de los servicios. Así, si el servidor falla o se está actualizando, la red no se cae. De mi propuesta se conservó la estrategia de caché y almacenamiento, y de la de Carol, el método VLSM y la matriz de tráfico.

[Topología del laboratorio GNS3 → foto de los equipos físicos]

> Ese diseño lo probamos primero en un laboratorio virtual en GNS3, con el mismo sistema del MikroTik y el mismo Ubuntu del servidor. Cuando funcionó, pasamos a lo físico cambiando un solo equipo a la vez: primero la Raspberry, después el MikroTik, luego el punto de acceso y por último la Starlink. Así, cada vez que algo fallaba, sabíamos exactamente dónde estaba el problema. Y después de cada cambio guardábamos un respaldo de la configuración.

---

## A3 — Detalle del direccionamiento (justo antes de la explicación de Carol de las VLAN, ≈ 5:28) · ≈ 40 s

[Tabla VLSM: VLAN 10 /28, VLAN 20 /27, VLAN 30 /25, rangos libres]

> El bloque 10.20.0.0/24 se dividió según cuántas personas usa cada grupo. La red pública, que es la más grande, tiene una /25, con 126 direcciones. Salud tiene una /27, con 30, y administración una /28, con 14. Quedan dos bloques libres para crecer.
>
> El DHCP lo da la Raspberry para las tres redes. Como la Raspberry solo está en la VLAN de administración, el MikroTik le reenvía las solicitudes de las otras dos con un relay DHCP.

---

## A4 — Pruebas que no se ven en el video (después de la prueba del firewall de Carol, ≈ 9:36) · ≈ 60 s

[Captura P12: 0,57 s → 0,002 s y TCP_MEM_HIT]

> Además de lo que se vio, hicimos otras pruebas en sesiones anteriores. En la caché de Squid, la primera descarga de un archivo tardó 0,57 segundos, y la segunda, servida desde la caché, 0,002 segundos.

[Capturas P13: regla desactivada → reactivada]

> Cuando apagamos Squid a propósito, en menos de diez segundos el MikroTik lo detectó, desactivó el desvío y los celulares siguieron navegando. Al encenderlo, el desvío se reactivó solo.

[Captura de la sesión del Hotspot con su cola de 2 Mbps]

> En la red pública, cada usuario queda limitado a 2 megabits de bajada, y salud tiene ancho de banda garantizado y prioridad.

[Respuesta 206 Partial Content]

> Y los videos están codificados en 720p a 1,2 megabits con el índice al inicio del archivo: empiezan de inmediato, se pueden adelantar y caben dentro del límite de cada usuario. No usamos Jellyfin porque la Raspberry no tiene codificador de video por hardware: transcodificar en vivo la saturaría, así que el video se prepara una sola vez y se sirve como un archivo normal.

---

## A5 — Resultados y cierre (al final) · ≈ 45 s

[Resumen: 15 de 15 pruebas de red, 4 de 4 de video, funciona sin Internet]

> En total se cumplieron las quince pruebas de red y servicios y las cuatro de video. La más importante fue la que no planeamos: dentro del laboratorio, la Starlink no tenía buena vista al cielo y casi no tuvo señal. Aun así, la comunidad siguió teniendo portal, guías de salud, Wikipedia y videos, que es justamente para lo que se diseñó la red.

[Trabajo futuro: disco de 2 TB, purga automática, modo online/offline, batería]

> Para operar en campo faltan un disco de 2 terabytes, la limpieza automática del contenido viejo, la conmutación automática entre modo en línea y sin conexión, y la batería con apagado ordenado. Nada de eso exige cambiar el diseño, solo ampliarlo.
>
> Todas las configuraciones, capturas y el informe están en nuestro repositorio. Muchas gracias, profesor.

[Cierre: nombres y enlace del repositorio]

---

## Cambios en el video de Carol (no necesitan audio)

- **4:34–4:46:** se corta la frase «información… de pacientes». El portal es público y no guarda datos de pacientes.
- **5:28–8:13** (explicación de Carol sobre la mesa del MikroTik): se pone encima la topología, la matriz de tráfico y el diagrama de la CDN, con el audio de Carol sin cambios.
- **Pantallas de terminal ilegibles:** recuadro con el resultado («servicios activos», «relay DHCP», «NTP sincronizado», «aislamiento OK»).
