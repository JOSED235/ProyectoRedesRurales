# 🌐 Proyecto Redes Rurales — Infraestructura de Redes 2

## 📋 Contexto del Proyecto

Este proyecto tiene como objetivo **desplegar una plataforma de atención móvil comunitaria** enfocada en la infraestructura de red necesaria para su operación en entornos rurales o con acceso limitado a Internet.

La plataforma debe funcionar como una **red local independiente** con capacidades de:
- **Portal cautivo** que segmente el acceso para distintos grupos de interés (comunidad, personal de salud, educadores, etc.)
- **Proxy/caché local** que permita acceso a contenido educativo, de salud y ocio incluso sin conexión a Internet
- **Servidor físico** basado en **Mini PC** o **Raspberry Pi** como nodo central de la red

---

## 🎯 Objetivo General

Desplegar una infraestructura de red que soporte la plataforma comunitaria permitiendo:
1. Acceso a Internet cuando esté disponible
2. Acceso a contenido cacheado localmente en modo **offline**
3. Segmentación de usuarios mediante portal cautivo
4. Distribución local de contenido multimedia (video, documentos, sitios web)

---

## 📦 Arquitectura General (Planeada)

```
[Internet / ISP]
       |
  [Raspberry Pi / Mini PC]
       |-- Squid Proxy (caché HTTP/HTTPS)
       |-- Servidor DNS/DHCP local
       |-- Portal Cautivo (Nginx / NoDogSplash / PfSense)
       |-- Servidor Multimedia (Jellyfin / Plex)
       |-- Almacenamiento local (2–4 TB)
       |
  [Clientes WiFi / LAN]
    - Comunidad general
    - Personal de salud
    - Educadores / estudiantes
```

---

## 📅 Fases del Proyecto y Rúbrica

El proyecto se divide en **3 fases de entrega**, cada una con sus propios criterios de evaluación:

---

### 🔵 Fase 1 — Plan de Proyecto

| Criterio | Beginning (1.0–2.9) | Developing (3.0–3.7) | Proficient (3.8–4.4) | Accomplished (4.5–5.0) |
|---|---|---|---|---|
| **Arquitectura de Red** | Diseño vago o técnicamente inviable. No define topología de red. | Define la topología pero omite detalles de direccionamiento o flujo de datos. | Diseño sólido con roles definidos para el servidor y los clientes. | Arquitectura detallada (L2/L3), optimizada para el hardware propuesto (RPi5/i5). |
| **Estrategia de Caché** | No especifica cómo se almacenará o refrescará el contenido. | Menciona herramientas (ej. Squid) pero no la lógica de actualización. | Describe claramente el proceso de descarga y persistencia de datos. | Plan avanzado: políticas de refresco de caché, gestión de HTTPS y jerarquía de almacenamiento. |
| **Cronograma y Recursos** | No hay hitos claros ni asignación de tareas. | Hitos generales sin tiempos realistas de implementación técnica. | Plan de trabajo estructurado con hitos para cada fase de desarrollo. | Ruta crítica definida con gestión de riesgos (ej. falta de luz o conectividad). |

---

### 🟡 Fase 2 — Prototipo

| Criterio | Beginning (1.0–2.9) | Developing (3.0–3.7) | Proficient (3.8–4.4) | Accomplished (4.5–5.0) |
|---|---|---|---|---|
| **Instalación y SO** | El sistema no arranca o tiene errores críticos de dependencias. | SO instalado pero con configuraciones de red por defecto e inestables. | Sistema operativo y servicios base (Squid/Docker/Nginx) estables. | OS optimizado para lectura/escritura en discos de 2–4TB; seguridad básica. |
| **Caché de Contenido Estático** | El sistema no guarda ni sirve contenido en modo local. | Solo sirve archivos de texto o imágenes pequeñas de forma errática. | El prototipo sirve sitios web estáticos y documentos PDF sin conexión. | Caché funcional de alta velocidad para sitios web populares y archivos educativos. |
| **Conectividad Local** | Los dispositivos clientes no pueden conectarse al servidor. | Conexión limitada a un solo dispositivo o requiere configuración manual compleja. | Los clientes se conectan y resuelven peticiones DNS locales hacia el caché. | DHCP/DNS local robusto; portal cautivo básico para acceso al contenido. |

---

### 🟢 Fase 3 — Sistema Plenamente Operacional

| Criterio | Beginning (1.0–2.9) | Developing (3.0–3.7) | Proficient (3.8–4.4) | Accomplished (4.5–5.0) |
|---|---|---|---|---|
| **Streaming de Video y Multimedia** | El video no carga o se interrumpe constantemente. | Video funcional pero con tiempos de carga (buffering) excesivos. | Streaming fluido de videos educativos almacenados localmente. | Servidor de streaming optimizado (ej. Plex/Jellyfin) con transcodificación si aplica. |
| **Gestión de Almacenamiento (2–4TB)** | Solo se usa una fracción mínima del disco o hay errores de montaje. | Almacenamiento montado pero sin estructura de directorios lógica. | Almacenamiento organizado con redundancia básica o gestión de cuotas. | Uso eficiente del almacenamiento; scripts automáticos para purga de contenido viejo. |
| **Interfaz de Usuario (Portal)** | El usuario debe usar comandos para acceder a los contenidos. | Interfaz rudimentaria (lista de carpetas/archivos) difícil de navegar. | Portal web intuitivo para navegar por las categorías (educación, salud, ocio). | Dashboard profesional, categorizado y con búsqueda local de contenidos. |
| **Rendimiento y Modo Desconectado** | El sistema falla totalmente cuando se desconecta de Internet. | Algunos contenidos fallan al no detectar conexión externa. | El sistema opera al 100% en modo offline para todo el contenido cacheado. | El sistema conmuta inteligentemente entre modo online (update) y offline. |

---

## 🛠️ Stack Tecnológico Propuesto

| Componente | Tecnología |
|---|---|
| Hardware | Raspberry Pi 5 / Mini PC con procesador i5 |
| Sistema Operativo | Raspberry Pi OS / Ubuntu Server |
| Proxy/Caché | Squid Proxy |
| Servidor Web | Nginx |
| Contenedores | Docker / Docker Compose |
| DNS/DHCP | dnsmasq / Pi-hole |
| Portal Cautivo | NoDogSplash / pfSense / Nodogsplash |
| Streaming | Jellyfin / Plex |
| Almacenamiento | 2–4 TB HDD/SSD externo |

---

## 📁 Estructura del Proyecto

```
ProyectoRedesRurales/
├── docs/                    # Enunciado y rúbrica del proyecto
├── fase1-plan/              # Documentos del plan de proyecto (Fase 1)
├── fase2-prototipo/         # Configuraciones y scripts del prototipo (Fase 2)
├── fase3-produccion/        # Sistema completo y documentación final (Fase 3)
├── configs/                 # Archivos de configuración (Squid, Nginx, dnsmasq, etc.)
├── scripts/                 # Scripts de automatización y mantenimiento
├── GEMINI.md                # Reglas del asistente IA para este proyecto
└── README.md                # Este archivo
```

---

## 👥 Equipo y Datos Académicos

- **Estudiante:** José David Rodríguez Pinilla (Código: `A00407151`)
- **Profesor:** Andrés Navarro Cadavid, Ph.D.
- **Curso:** Infraestructura de Redes 2
- **Institución:** Universidad Icesi, Cali, Colombia

---

## 📌 Estado Actual

- [x] Lectura y comprensión del enunciado
- [x] Análisis de la rúbrica por fases
- [ ] Fase 1: Plan de proyecto
- [ ] Fase 2: Prototipo funcional
- [ ] Fase 3: Sistema plenamente operacional