# 🌐 Proyecto Redes Rurales — Infraestructura de Redes 2

> **Diseño e Implementación de Infraestructura de Red Local Autónoma para Atención Móvil Comunitaria en Entornos Rurales**  
> **Universidad Icesi** — Departamento de Tecnologías de Información y Comunicaciones  
> **Materia:** Infraestructura de Redes 2  
> **Estudiante:** José David Rodríguez Pinilla (Código: `A00407151` — `jdrpjd@gmail.com`)  
> **Profesor:** Andrés Navarro Cadavid, Ph.D.  

---

## 📋 1. Contexto y Descripción del Proyecto

El objetivo de este proyecto es diseñar y desplegar la infraestructura de red local para una **unidad móvil de atención comunitaria** que opera en áreas rurales de difícil acceso. Estas zonas enfrentan problemas críticos como:
- **Ausencia o intermitencia severa de conectividad a Internet** (cobertura móvil limitada, alto costo de enlaces satelitales).
- **Inestabilidad del fluido eléctrico** (alimentación dependiente de la batería del vehículo y sistemas auxiliares).
- **Necesidad de atender grupos heterogéneos:** Comunidad general (navegación educativa/salud), Educadores (material pedagógico) y Personal de Salud (historias clínicas confidenciales).

La red opera como un sistema autónomo basado en la filosofía ***offline-first***: funciona al 100% en aislamiento total gracias a un almacenamiento masivo local de 2–4 TB y conmuta inteligentemente a modo *online* cuando detecta enlace LTE/satelital para realizar sincronizaciones incrementales diferidas.

---

## 🎯 2. Requisitos y Decisiones de Diseño

| ID | Requisito | Decisión Técnica de Ingeniería |
|---|---|---|
| **RQ1** | Red autónoma con acceso a Internet oportunista | Raspberry Pi 5 como gateway con NAT/firewall (`nftables`); WAN mediante adaptador USB 3 a Gigabit Ethernet. |
| **RQ2** | Acceso diferenciado por grupo de interés | Portal cautivo único (`openNDS`) con perfiles dinámicos en L3 + SSID cifrado WPA3 para salud. |
| **RQ3** | Proxy/Caché local de alto rendimiento | Squid Proxy en el host con jerarquía en RAM, NVMe (`rock`) y SSD (`aufs`), y modo híbrido HTTPS (*peek and splice*). |
| **RQ4** | Almacenamiento masivo (2–4 TB) | SSD USB 3 portátil de 2 TB (antivibración/bajo consumo, ampliable a 4 TB con un 2.º SSD) + NVMe para SO y BD. |
| **RQ5** | Operación offline integral | Conmutación automática (*heartbeat* cada 30s con histéresis) que activa `offline_mode on` en Squid y DNS local. |
| **RQ6** | Tolerancia a cortes eléctricos | Batería auxiliar LiFePO₄ 12V/20Ah con cargador DC-DC, monitor de voltaje para apagado ordenado y `ext4` con `data=ordered`. |
| **RQ7** | Protección de datos clínicos | Aislamiento L2/L3: SSID 2 (`Salud-Segura`) con WPA3-SAE, VLAN 10 dedicada, TLS interno y base de datos cifrada. |
| **RQ8** | Plataforma de atención comunitaria | Aplicación Spring Boot 3.x (Java 21) en contenedor Docker multi-arch (`linux/arm64`), PostgreSQL en NVMe y cola *outbox* sincronizable. |

---

## 📐 3. Arquitectura del Sistema

### 3.1 Topología Física y Lógica
```
                      [ Internet / ISP (LTE / Satélite) ]
                                      |
                           [ Módem / Router LTE ]
                                      | (WAN: eth1 - USB3 GbE)
        +-----------------------------v-----------------------------+
        |                 Raspberry Pi 5 (8 GB RAM)                |
        |  - Host: nftables (NAT/FW), dnsmasq (DNS/DHCP), openNDS    |
        |          Squid (Proxy/Caché), Nginx (Reverse Proxy)       |
        |  - Storage: M.2 NVMe (SO/BD/Rock) + SSD USB 3 (2-4 TB)   |
        |  - Containers: Spring Boot, PostgreSQL, Jellyfin, Kiwix   |
        +-----------------------------+-----------------------------+
                                      | (Trunk 802.1Q: eth0)
                           [ Switch Gestionable L2 ]
                           /                       \
        (Trunk VLAN 10,30,99)                     (Acceso VLAN 99)
                 |                                        |
       [ Access Point Wi-Fi 6 ]                   [ Laptop Admin SSH ]
        /                    \
  (SSID 1: Abierto)     (SSID 2: WPA3-SAE)
   VLAN 30 (Portal)      VLAN 10 (Salud Segura)
         |                        |
  [ Celulares / Tablets ]  [ Tablets Clínicas ]
   - Comunidad (2h / 2Mbps)  - Personal de Salud
   - Educadores (12h / 5Mbps)  (Acceso directo a
   - Salud por portal           plataforma interna)
```

### 3.2 Segmentación de Red (L2 / L3)
La red utiliza el direccionamiento privado `10.10.0.0/16` con VLSM y sufijos `.internal` (RFC 6762 / IETF private TLD):

| Segmento / VLAN | Subred CIDR | Gateway | Rango DHCP (Capacidad) | Propósito y Control |
|---|---|---|---|---|
| **VLAN 10: Salud Segura** | `10.10.10.0/24` | `10.10.10.1` | `.50` -- `.200` (151 leases, 12h) | Equipos clínicos, WPA3, sin portal cautivo, acceso a `salud.internal`. |
| **VLAN 30: Portal Cautivo**| `10.10.30.0/23` | `10.10.30.1` | `10.10.30.50` -- `10.10.31.250` (~457 leases, 2h) | Comunidad y educadores, SSID abierto, interceptado por openNDS. |
| **VLAN 99: Gestión** | `10.10.99.0/28` | `10.10.99.1` | `.5` -- `.14` (10 estáticas) | Administración cableada del AP, Switch y consola SSH del nodo. |
| **VLAN 20: Reserva** | `10.10.20.0/24` | `10.10.20.1` | - | Reservada para crecimiento (segundo AP o aula móvil). |
| **WAN (Uplink LTE)** | DHCP ISP | Dinámico | 1 IP pública/CGNAT | Interfaz `eth1` (USB 3 a GbE) con masquerade NAT en `nftables`. |

### 3.3 Presupuesto de Memoria RAM (Raspberry Pi 5 - 8 GB)
| Servicio | Entorno | RAM Asignada |
|---|---|---|
| Sistema Operativo (Debian) + Docker Engine | Host nativo | 0.80 GB |
| Squid Proxy (`cache_mem` 1 GB + índice en RAM y proceso) | Host nativo | 1.50 GB |
| Servicios de red (`dnsmasq`, `openNDS`, `Nginx`) | Host nativo | 0.30 GB |
| Plataforma de atención (Spring Boot 3.x JVM `-Xmx768m`) | Contenedor Docker | 1.00 GB |
| Base de datos PostgreSQL (con `shared_buffers` 256MB) | Contenedor Docker | 0.75 GB |
| Servidor multimedia Jellyfin (*direct play*, sin transcodificación en vivo) | Contenedor Docker | 0.80 GB |
| Servidor educativo Kolibri | Contenedor Docker | 0.70 GB |
| Servidor Kiwix-serve (Wikipedia/ZIM offline) | Contenedor Docker | 0.30 GB |
| **Total Comprometido** | | **6.15 GB** |
| **Memoria Libre para Caché de Páginas del Kernel (I/O)** | | **1.85 GB** |

---

## 💾 4. Estrategia de Almacenamiento y Caché Masivo (2–4 TB)

### 4.1 Jerarquía de Almacenamiento
1. **Nivel 1 (RAM):** `cache_mem` de 1024 MB en Squid y tabla DNS en memoria.
2. **Nivel 2 (NVMe M.2 - 256 a 512 GB):** SO, base de datos PostgreSQL, volúmenes Docker y directorio `rock` de Squid para objetos pequeños ($\le$256 KB).
3. **Nivel 3 (SSD USB 3 - 2 TB a 4 TB):** Directorio `aufs` de Squid (200 GB para objetos grandes), repositorio Kiwix ZIM (100 GB), Kolibri (150 GB), videos educativos pre-transcodificados Jellyfin (1000 GB), manuales PDF (20 GB) y respaldos (100 GB).

### 4.2 Políticas de Caché y Manejo de HTTPS
- **HTTP (Puerto 80):** Intercepción transparente redirigida al puerto `3129` de Squid vía `nftables`.
- **HTTPS (Puerto 443):** Modo **SslPeekAndSplice** en puerto `3130`. Squid inspecciona el SNI del *ClientHello* para aplicar listas de control de acceso y registrar dominios, dejando pasar el túnel TLS intacto para preservar la privacidad y evitar instalar certificados CA en dispositivos de la comunidad.
- **Espejos Locales Curados:** Contenido masivo (Wikipedia, cursos, videos) servido directamente desde Nginx local en dominios `*.internal` sin requerir conexión a Internet.
- **Políticas de Refresco (`refresh_pattern`):** Retención agresiva mínima de 7 días (10080 min) y máxima de 30 días para archivos estáticos (`pdf`, `epub`, `zim`, `mp4`, `webm`, `jpg`, `png`, `css`, `js`). Reemplazo mediante algoritmo `heap LFUDA` (Least Frequently Used with Dynamic Aging).

---

## ⚡ 5. Sistema de Energía y Resiliencia
- **Consumo Total:** ~27 W típico / ~39 W pico (RPi5 + NVMe + SSD + AP Wi-Fi 6 + Switch + Router LTE).
- **Alimentación:** Batería auxiliar LiFePO₄ de 12V/20Ah (~256 Wh, ~185 Wh útiles al 90% de eficiencia).
- **Autonomía:** **~6.8 horas** en uso típico y **~4.7 horas** en el peor caso con el motor apagado. En marcha, se carga mediante convertidor DC-DC conectado al alternador.
- **Protección del Almacenamiento:** Monitor de voltaje que activa un apagado ordenado del sistema (`shutdown -h now`) al caer por debajo del umbral de descarga crítica, evitando la corrupción del SSD.

---

## 📅 6. Plan de Trabajo, Cronograma y Fases (11 Semanas)

Dado que el proyecto se ejecuta con un **único integrante**, la planificación aplica nivelación de recursos serializando la ruta crítica en 11 semanas, con compras y descargas en segundo plano:

```
Semana:    S1   S2   S3   S4   S5   S6   S7   S8   S9   S10   S11
Fase 1:   [T1: Diseño/Plan]
Fase 2:                   [T2:SO] [T3:Red] [T4:Squid] [T5:Portal]
Fase 3:                                       [T6:App] [T7:Media] [T8-T9] [T10:Test]
Compras:       (Lote 1)---^   (Lote 2)---^             (Lote 3)---^
```

### 6.1 Actividades de la Ruta Crítica
- **T1 (Sem. 1–3):** Diseño de arquitectura, informe IEEE Fase 1, topología, matriz de riesgos y plan de compras. *(Hito: Informe Fase 1)*.
- **T2 (Sem. 4):** Instalación de Debian/Raspberry Pi OS, optimización de kernel, particionado y montaje de SSD 2 TB, Docker.
- **T3 (Sem. 5):** Configuración de red base: VLANs 802.1Q, reglas `nftables`, `dnsmasq` (DHCP/DNS) y enlace AP.
- **T4 (Sem. 6):** Despliegue de Squid (HTTP/HTTPS peek+splice), Nginx y caché de contenido estático (HITs verificados).
- **T5 (Sem. 7):** Integración del portal cautivo `openNDS` con perfiles (Comunidad, Educador, Salud). *(Hito: Prototipo Fase 2)*.
- **T6 (Sem. 8):** Despliegue de plataforma Spring Boot 3.x en contenedor Docker y base de datos PostgreSQL.
- **T7 (Sem. 9):** Integración de servicios de contenido: Kiwix, Kolibri, servidor Jellyfin y pre-transcodificación de video.
- **T8–T9 (Sem. 10):** Dashboard de usuario con búsqueda local y servicio de conmutación automática online/offline.
- **T10 (Sem. 11):** Pruebas de carga, autonomía de batería, endurecimiento de seguridad y entrega final. *(Hito: Sistema Plenamente Operativo Fase 3)*.

### 6.2 Plan de Compras Escalonado (BOM)
- **Lote 1 (Sem. 2 - USD $380):** RPi5 8GB, Active Cooler, fuente 27W, M.2 HAT+ con NVMe 256-512GB, SSD USB 3 de 2TB, adaptador USB 3 a GbE.
- **Lote 2 (Sem. 3 - USD $110):** Access Point Wi-Fi 6 con VLAN y multi-SSID, Switch gestionable de 5 puertos.
- **Lote 3 (Sem. 7 - USD $200):** Router LTE con antenas externas, batería LiFePO₄ 12V/20Ah, convertidor DC-DC 12V a 5V/5A.
- **Total Inversión Base:** USD $690 (+ 15% contingencia = **USD $794**).

---

## 🛡️ 7. Matriz de Gestión de Riesgos Principales

| Riesgo | Prob. | Imp. | Nivel | Mitigación Técnica |
|---|:---:|:---:|:---:|---|
| **Corte eléctrico repentino en la unidad móvil** | 4 | 5 | **20** | Batería LiFePO₄ + cargador DC-DC, script de apagado ordenado por umbral de voltaje y sistema `ext4` con `data=ordered`. |
| **Falta total de enlace satelital o LTE** | 5 | 4 | **20** | Modo `offline_mode on` automático en Squid, DNS split-horizon interno y precarga inicial de 1.3 TB de contenido curado. |
| **Sobrecarga de trabajo (único integrante)** | 4 | 4 | **16** | Nivelación secuencial de recursos, desarrollo previo en laptop con Docker Buildx y alcance modular (Esencial / Deseable / Opcional). |
| **Falla del SSD o corrupción del sistema** | 3 | 5 | **15** | Uso de SSD (resistente a vibraciones mecánicas del vehículo), particiones separadas por servicio y respaldos automatizados. |
| **Saturación del disco de 2 TB** | 3 | 4 | **12** | Cuotas estrictas por partición, purga LFUDA automática en Squid y scripts `systemd timer` para eliminar temporales al superar el 85%. |
| **Exposición de datos clínicos de salud** | 2 | 5 | **10** | SSID 2 exclusivo con cifrado WPA3-SAE, VLAN 10 aislada por firewall `nftables` y HTTPS interno sin acceso desde la red comunitaria. |

---

## 📁 8. Estructura del Repositorio

```
ProyectoRedesRurales/
├── docs/                             # Documentación y rúbrica oficial
│   ├── Enunciado.txt                 # Enunciado oficial del proyecto
│   ├── Rúbrica Proyecto...xlsx       # Criterios de evaluación en 3 fases
│   └── InformePFinal.tex             # Documento maestro IEEE con diseño exhaustivo
├── fase1-plan/                       # Entregables de la Fase 1
│   └── informe_fase1.tex             # Informe IEEE listo para compilar en Overleaf
├── configs/                          # Plantillas de configuración (Squid, dnsmasq, nftables, Nginx)
├── scripts/                          # Scripts de conmutación offline/online y purga de almacenamiento
├── GEMINI.md                         # Reglas operativas del asistente IA (Siempre en Español)
├── skills.md                         # Catálogo de habilidades y competencias técnicas del proyecto
└── README.md                         # Contexto global y especificación técnica de la infraestructura
```

---

## 📌 9. Estado del Proyecto

- [x] **Fase 1: Plan de Proyecto**
  - [x] Arquitectura de Red L2/L3 optimizada para Raspberry Pi 5.
  - [x] Estrategia de Caché jerárquica con Squid y almacenamiento 2–4 TB.
  - [x] Cronograma de 11 semanas, ruta crítica y presupuesto de compras escalonado.
  - [x] Matriz de gestión de riesgos (energía, enlace, disco y seguridad clínica).
  - [x] Informe IEEE compilable en Overleaf ([`docs/InformePFinal.tex`](file:///C:/Users/Fa1097la/OneDrive%20-%20Universidad%20Icesi/Sexto%20Semestre/Infraestructura2/ProyectoRedesRurales/docs/InformePFinal.tex) / [`fase1-plan/informe_fase1.tex`](file:///C:/Users/Fa1097la/OneDrive%20-%20Universidad%20Icesi/Sexto%20Semestre/Infraestructura2/ProyectoRedesRurales/fase1-plan/informe_fase1.tex)).
- [ ] **Fase 2: Prototipo Funcional** (SO base, almacenamiento 2 TB, VLANs, Squid estático y portal cautivo).
- [ ] **Fase 3: Sistema Plenamente Operacional** (Plataforma Spring Boot, Jellyfin, Dashboard con búsqueda y conmutación automática).