# Fase 3 — Sistema plenamente operacional

Parte del prototipo de la Fase 2 ([`fase2-prototipo/README.md`](../fase2-prototipo/README.md)). La evaluación criterio por criterio está en la Tabla VIII del [informe final](../docs/InformeFinal.pdf).

## Hecho

| Criterio de la rúbrica | Qué hay | Nivel estimado |
|---|---|---|
| Streaming de video | CDN local en Nginx: MP4 720p ≤ 1,2 Mbps con `faststart`, peticiones de rango (206), catálogo `videos.html` (Fase 2.4, pruebas V1–V4) | Proficient (sin Jellyfin, por decisión) |
| Gestión de almacenamiento | `/srv/cdn` con directorios por servicio y categoría, `nofail` + `RequiresMountsFor`, caché de Squid con tope y LFUDA | Proficient (faltan cuotas y purga) |
| Interfaz de usuario | Portal con categorías Educación/Salud/Ocio, búsqueda local y búsqueda de la Wikipedia integrada | Accomplished |
| Rendimiento offline | Todo el contenido local funciona con la Starlink sin señal (P11, V3); Squid se omite solo si cae (P13) | Proficient (falta conmutación online/offline) |

## Pendiente

## Alcance según la rúbrica

- ~~Streaming de video optimizado~~: hecho con Nginx (Fase 2.4). Jellyfin se descartó porque la RPi5 no tiene codificador H.264 por hardware.
- Almacenamiento de 2–4 TB organizado, con cuotas y scripts automáticos de purga.
- Dashboard categorizado (educación, salud, ocio) con búsqueda local, sobre el portal `portal.hub.lan`. Base hecha el 19/11 en [`configs/servidor/www/index.html`](../configs/servidor/www/index.html): categorías, búsqueda local sin tildes, documentos leídos del autoindex de `/pdf/<categoría>/` y búsqueda en Kiwix. Hecho: portal pulido con fuentes locales, búsqueda de Kiwix dentro del portal y catálogo de video.
- Conmutación inteligente entre modo online (actualización) y offline.
- Energía: consumo real, autonomía y apagado ordenado al 15 % de batería.

## Pendientes heredados de la Fase 2.3

- SSD de 2–4 TB definitivo y caché de Squid de 50–100 GB (`cache_dir aufs /srv/cdn/squid 51200 …`).
- Pila del RTC en el conector BAT y `dtparam=rtc_bbat_vchg=3000000` en `/boot/firmware/config.txt`, para tener hora sin Internet tras cada apagado.
- Sincronización una vez por conexión y aviso a las aplicaciones por MQTT (Mosquitto, puerto `8883` ya abierto para la VLAN 20 en el firewall).
- Telemetría con Datadog.
- Certificado real con certbot (DNS-01) cuando el profesor confirme el dominio.
- CA de pruebas con `nameConstraints` limitada a `hub.lan` (ver Fase 2, Siguiente).
- Docker solo para los servicios nuevos que lo justifiquen (Jellyfin, Mosquitto), con imágenes `linux/arm64`.
