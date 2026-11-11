# ============================================================================
# hub-ccr2004.rsc — Configuración del hub en el MikroTik CCR2004-16G-2S+ prestado
# Fuente: documento "Fase 2.2 — MikroTik CCR2004" (Parte C2), 05/11/2026.
#
# Es la misma lógica de hub-base.rsc; solo cambian los puertos, porque
# ether1 y ether2 tienen conectados el kit y el AP del otro grupo:
#   ether9  = WAN (portátil en modo "Compartida", simula Starlink)  -> plan: ether1
#   ether10 = servidor hub Raspberry Pi 5 (acceso VLAN 10)          -> plan: ether2
#   ether11 = troncal AP UniFi (V10 sin etiqueta, V20/V30 etiq.)    -> plan: ether3
#   ether12 = portátil de administración (acceso VLAN 10)           -> plan: ether4
#   Resto de puertos y SFP+ deshabilitados.
#
# ANTES: respaldar la configuración del otro grupo (.backup + /export) y
# resetear: /system reset-configuration no-defaults=yes skip-backup=yes
# Pegar por consola serial (/dev/ttyUSB0, 115200) bloque por bloque.
# La contraseña de admin se pone a mano: no se guarda en el repositorio.
# Aún NO incluye firewall entre VLAN, relay DHCP, Hotspot ni colas (Fase 2).
# ============================================================================

# --- Bloque 1: identidad y hora ---------------------------------------------
/system identity set name=hub-mikrotik
/system clock set time-zone-name=America/Bogota

# --- Bloque 2: puertos (todo deshabilitado salvo los del hub) ---------------
/interface ethernet set [find] disabled=yes
/interface ethernet set [find default-name=ether9] disabled=no comment="WAN: portatil (simula Starlink)"
/interface ethernet set [find default-name=ether10] disabled=no comment="Servidor hub Raspberry Pi (VLAN 10)"
/interface ethernet set [find default-name=ether11] disabled=no comment="AP UniFi (troncal VLAN 10/20/30)"
/interface ethernet set [find default-name=ether12] disabled=no comment="Portatil admin (VLAN 10)"

# --- Bloque 3: bridge y VLAN (vlan-filtering al final) ----------------------
/interface bridge add name=br-lan vlan-filtering=no
/interface bridge port
add bridge=br-lan interface=ether10 pvid=10
add bridge=br-lan interface=ether11 pvid=10
add bridge=br-lan interface=ether12 pvid=10
/interface bridge vlan
add bridge=br-lan vlan-ids=10 tagged=br-lan untagged=ether10,ether11,ether12
add bridge=br-lan vlan-ids=20 tagged=br-lan,ether11
add bridge=br-lan vlan-ids=30 tagged=br-lan,ether11
/interface vlan
add name=vlan10-admin interface=br-lan vlan-id=10
add name=vlan20-salud interface=br-lan vlan-id=20
add name=vlan30-publica interface=br-lan vlan-id=30
/interface bridge set br-lan vlan-filtering=yes

# --- Bloque 4: gateways, WAN por DHCP, DNS, NAT y NTP -----------------------
/ip address
add interface=vlan10-admin address=10.20.0.161/28
add interface=vlan20-salud address=10.20.0.129/27
add interface=vlan30-publica address=10.20.0.1/25
/ip dhcp-client add interface=ether9 disabled=no
/ip dns set servers=1.1.1.1,9.9.9.9
/ip firewall nat add chain=srcnat src-address=10.20.0.0/24 out-interface=ether9 action=masquerade comment="NAT del sitio (resumen 10.20.0.0/24)"
/system ntp client set enabled=yes
/system ntp client servers add address=pool.ntp.org

# --- Bloque 5: servicios de gestión (quedan ssh, winbox y www) --------------
/ip service disable telnet,ftp,api,api-ssl
