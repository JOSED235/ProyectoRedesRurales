# Fase 3 — Sistema plenamente operacional

Pendiente. Parte del estado de la Fase 2.3 ([`fase2-prototipo/README.md`](../fase2-prototipo/README.md)).

## Alcance según la rúbrica

- Streaming de video optimizado (Jellyfin desde `/srv/cdn/video`, sin transcodificación en vivo en la RPi5).
- Almacenamiento de 2–4 TB organizado, con cuotas y scripts automáticos de purga.
- Dashboard categorizado (educación, salud, ocio) con búsqueda local, sobre el portal `portal.hub.lan`. Base hecha el 19/11 en [`configs/servidor/www/index.html`](../configs/servidor/www/index.html): categorías, búsqueda local sin tildes, documentos leídos del autoindex de `/pdf/<categoría>/` y búsqueda en Kiwix. Falta: Jellyfin en Ocio y contenido real.
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
