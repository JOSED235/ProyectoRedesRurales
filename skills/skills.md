# 🛠️ Habilidades y Competencias Técnicas — Proyecto Redes Rurales

Este documento define el catálogo de habilidades, conocimientos especializados y herramientas técnicas requeridas para el desarrollo exitoso del proyecto de infraestructura de redes comunitarias rurales (Universidad Icesi - Infraestructura de Redes 2).

---

## 🌐 1. Redes y Conectividad (L2 / L3)
* **Diseño y Segmentación de Topologías de Red:**
  * Segmentación por VLANs o subredes lógicas para distintos grupos de interés (comunidad general, personal de salud, educadores/administración).
  * Políticas de direccionamiento IP (IPv4 CIDR, pools DHCP diferenciados).
* **Servicios de Red Base (DHCP & DNS):**
  * Despliegue y configuración de `dnsmasq` o `Pi-hole` / `Unbound`.
  * Redirección y resolución de nombres en entornos sin salida a Internet (DNS local para dominios internos y captive portal detection).
* **Enrutamiento, Firewall e Inspección de Tráfico:**
  * Configuración de reglas `iptables` / `nftables` para reenvío de paquetes, NAT y control de acceso.
  * Implementación de Portal Cautivo (`openNDS`, `NoDogSplash` o gateway cautivo mediante Nginx/iptables).

---

## 💾 2. Proxy, Caché y Operación Offline
* **Proxy y Políticas de Almacenamiento Caché:**
  * Configuración avanzada de `Squid Proxy` (modos explícito y transparente).
  * Definición de jerarquías de almacenamiento (`ufs`, `aufs`, `rock`).
  * Políticas de expiración y refresco de caché (`refresh_pattern`) para sitios populares, librerías estáticas, paquetes y documentos educativos (PDFs).
  * Gestión de tráfico seguro HTTPS (SSL Bump / SslBump Peek and Splice o espejos locales de contenido).
* **Mecanismos de Sincronización y Descarga Diferida:**
  * Estrategias de conmutación inteligente modo Online (actualización/sync) vs. modo Offline (100% autónomo).
  * Herramientas de mirroring local y descarga programada (`rsync`, `wget`, `httrack`, `Kiwix` para Wikipedia offline).

---

## 🖥️ 3. Administración de Sistemas Linux y Optimización de Hardware
* **Sistemas Operativos para Dispositivos Limitados:**
  * Administración de `Ubuntu Server` o `Raspberry Pi OS (Debian)` optimizados para arquitecturas ARM64 (Raspberry Pi 5) o x86_64 (Mini PC Intel Core i5).
  * Parámetros de kernel para ahorro de energía, estabilidad térmica y memoria RAM limitada (Swappiness, zram, tuning sysctl).
* **Gestión de Almacenamiento Masivo (2–4 TB):**
  * Particionamiento y formatos de archivos (`ext4`, `xfs`, `Btrfs`) optimizados para lecturas concurrentes y archivos de gran tamaño.
  * Montaje persistente vía `/etc/fstab` con opciones seguras (`noatime`, cuotas de disco).
  * Scripts en Bash/Python para monitorización del disco, rotación de logs y purga automática de contenido obsoleto basada en marcas de agua (LRU - Least Recently Used).

---

## 🐳 4. Virtualización y Despliegue de Servicios (DevOps / Contenedores)
* **Docker & Docker Compose:**
  * Modularización de servicios en contenedores independientes (Squid, Nginx, Jellyfin, Dashboard Web, DNS).
  * Configuración de redes internas en Docker (`bridge`, `macvlan`, `host`) y volúmenes persistentes vinculados al almacenamiento masivo externo.
  * Políticas de reinicio automático ante cortes intempestivos de energía (`restart: always` / `unless-stopped`).
* **Servidores Web e Interfaces de Usuario:**
  * Configuración de `Nginx` como reverse proxy y servidor de contenido estático de alto rendimiento.
  * Desarrollo del Dashboard/Portal de bienvenida intuitivo, categorizado (Salud, Educación, Ocio) con buscador de recursos locales.

---

## 🎬 5. Streaming Multimedia y Distribución de Contenido
* **Servidores de Streaming Multimedia Local:**
  * Despliegue y afinamiento de `Jellyfin` (o `Plex`) para distribución fluida en redes locales WiFi/LAN.
  * Gestión y optimización de códecs (H.264/AAC) para evitar sobrecarga de transcodificación en el CPU de la Raspberry Pi o Mini PC.

---

## 🛡️ 6. Planificación, Gestión de Riesgos y Documentación
* **Continuidad de Servicio y Contingencias:**
  * Planes de contingencia ante caídas de fluido eléctrico, corrupción de almacenamiento y pérdida total de enlace ISP.
* **Documentación Técnica de Ingeniería:**
  * Diagramas de arquitectura formales (topología física y lógica en Mermaid/Draw.io).
  * Justificación técnica de decisiones acorde a la rúbrica del curso.

---

> ℹ️ **Nota de Interacción:** Todas las interacciones, explicaciones técnicas, manuales y comentarios de código se mantendrán rigurosamente en **español**, tal como lo estipula la directiva principal del proyecto.
