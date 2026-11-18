# ============================================================================
# hub-base.rsc — Configuración base del MikroTik (RouterOS 7) del hub rural
# Fuente: documento "Fase 1.2 — Laboratorio virtual en GNS3" (sección 6.5).
# Probado en MikroTik CHR 7.25 el 27/10/2026.
#
# IMPORTANTE: pegar SIEMPRE por consola (no por red): al activar
# vlan-filtering se puede perder la conexión de gestión.
# El /export real del MikroTik físico está en hub-ccr2004-2026-11-17.rsc.
# Aún NO incluye Hotspot, colas, relay DHCP ni firewall entre VLAN (Fase 2).
# ============================================================================

/system identity set name=hub-mikrotik

# --- Bridge con filtrado de VLAN (se activa al final) ----------------------
# ether1 = WAN (Starlink / nodo NAT en GNS3)
# ether2 = servidor hub (acceso VLAN 10)
# ether3 = troncal hacia el AP UniFi (VLAN 10 sin etiqueta + 20 y 30 etiquetadas)
# ether4 = portátil de administración (acceso VLAN 10)
# ether5 = libre, deshabilitado
/interface bridge add name=br-lan vlan-filtering=no
/interface bridge port
add bridge=br-lan interface=ether2 pvid=10
add bridge=br-lan interface=ether3 pvid=10
add bridge=br-lan interface=ether4 pvid=10
/interface bridge vlan
add bridge=br-lan vlan-ids=10 tagged=br-lan untagged=ether2,ether3,ether4
add bridge=br-lan vlan-ids=20 tagged=br-lan,ether3
add bridge=br-lan vlan-ids=30 tagged=br-lan,ether3
/interface vlan
add name=vlan10-admin interface=br-lan vlan-id=10
add name=vlan20-salud interface=br-lan vlan-id=20
add name=vlan30-publica interface=br-lan vlan-id=30
/interface bridge set br-lan vlan-filtering=yes

# --- Gateways de cada VLAN (router-on-a-stick) -----------------------------
/ip address
add interface=vlan10-admin address=10.20.0.161/28
add interface=vlan20-salud address=10.20.0.129/27
add interface=vlan30-publica address=10.20.0.1/25

# --- DNS del propio MikroTik (temporal, hasta que el hub tenga dnsmasq) -----
/ip dns set servers=1.1.1.1,9.9.9.9

# --- NAT de todo el sitio hacia la WAN --------------------------------------
/ip firewall nat add chain=srcnat src-address=10.20.0.0/24 out-interface=ether1 action=masquerade

# --- Puerto libre deshabilitado ---------------------------------------------
/interface ethernet disable ether5
