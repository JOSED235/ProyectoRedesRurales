# Reglas del Asistente — Proyecto Redes Rurales

## Idioma

- **Siempre responder en español**, sin excepción, incluso si el usuario escribe en inglés.
- Usar terminología técnica correcta en español cuando exista. Si el término técnico no tiene traducción natural, usar el término en inglés con una breve explicación la primera vez.

## Contexto del Proyecto

Este es un proyecto universitario de **Infraestructura de Redes 2** en la **Universidad Icesi**.
El objetivo es desplegar una infraestructura de red para una plataforma de atención móvil comunitaria rural, con:
- Portal cautivo para segmentación de usuarios
- Proxy/caché local con Squid
- Servidor basado en Raspberry Pi 5 o Mini PC
- Almacenamiento local de 2–4 TB
- Funcionalidad offline completa

**Diseño vigente (consolidado):** Starlink Mini → MikroTik RouterOS 7 (router-on-a-stick, NAT) → UniFi UAP-AC-M + Raspberry Pi 5 "hub" (Ubuntu Server 24.04). Bloque `10.20.0.0/24`: VLAN 10 Administración `10.20.0.160/28`, VLAN 20 Salud `10.20.0.128/27`, VLAN 30 Pública `10.20.0.0/25`. Ver `README.md` y `.claude/skills/ingeniero-redes-rurales/SKILL.md`. Las versiones individuales de la Fase 1 (`fase1-plan/version-*`) son históricas. Estado de la Fase 2 y lista para el laboratorio: `fase2-prototipo/README.md` y `fase2-prototipo/ARRANQUE-LAB.md`.

## Comportamiento General

- Ser conciso pero completo en las explicaciones técnicas.
- Siempre contextualizar las respuestas al proyecto de redes rurales.
- Antes de sugerir una solución, considerar las restricciones de hardware (RPi5 / Mini PC i5).
- Cuando se generen archivos de configuración, agregar comentarios explicativos en español.
- Avisar si una decisión puede afectar el rendimiento en hardware limitado.
