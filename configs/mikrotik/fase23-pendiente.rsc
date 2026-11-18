# ============================================================================
# fase23-pendiente.rsc — Lo que falta en el MikroTik para cerrar la Fase 2.3
# Fuente: Fase2.3_Servicios_AP_Portal_Cautivo.pdf, pasos 7 y 8.
# Se aplica DESPUÉS de cargar hub-ccr2004-2026-11-17.backup.
#
# NO es para /import de una vez. Pegar por bloques, en orden, por SSH
# (ssh admin@10.20.0.161) o por consola serial, comprobando cada bloque.
#
# Antes de pegar:
#   1. Subir hub.crt y hub.key (ver paso 7.1 en ARRANQUE-LAB.md).
#   2. Reemplazar CAMBIAR_CLAVE_SALUD por la clave de los usuarios de salud.
#      No se guarda en el repositorio porque es público.
# ============================================================================

# --- 7.1 Certificado comodín *.hub.lan (firmado por la CA de pruebas) -------
/certificate import file-name=hub.crt passphrase=""
/certificate import file-name=hub.key passphrase=""
# Debe salir hub.crt_0 con las letras K y T (tiene llave y es de confianza)
/certificate print
/file remove hub.key

# --- 7.2 Hotspot (portal cautivo) -------------------------------------------
# DNS del MikroTik: atiende a los usuarios antes de iniciar sesión y pregunta a la Raspberry
/ip dns set servers=10.20.0.162 allow-remote-requests=yes
# Perfiles de usuario (los límites del grupo se completan en el bloque 8.2)
/ip hotspot user profile add name=publica rate-limit=1M/2M shared-users=1 session-timeout=2h
/ip hotspot user profile add name=salud shared-users=2 session-timeout=8h
# Perfiles de los portales: pública con botón de prueba de 2 h; salud con usuario
/ip hotspot profile add name=hs-publica hotspot-address=10.20.0.1 dns-name=wifi-publica.hub.lan login-by=https,trial ssl-certificate=hub.crt_0 trial-uptime-limit=2h trial-user-profile=publica
/ip hotspot profile add name=hs-salud hotspot-address=10.20.0.129 dns-name=wifi-salud.hub.lan login-by=https ssl-certificate=hub.crt_0
# Un portal por VLAN; las IP las sigue dando la Raspberry por relay (address-pool=none)
/ip hotspot add name=hotspot-publica interface=vlan30-publica profile=hs-publica address-pool=none disabled=no
/ip hotspot add name=hotspot-salud interface=vlan20-salud profile=hs-salud address-pool=none disabled=no
# Usuarios de salud (datos simulados; se guardan en el MikroTik, funcionan sin Internet)
/ip hotspot user add name=enfermera01 password=CAMBIAR_CLAVE_SALUD profile=salud server=hotspot-salud
/ip hotspot user add name=promotor01 password=CAMBIAR_CLAVE_SALUD profile=salud server=hotspot-salud
# El contenido local (portal, PDF, Wikipedia) se ve sin iniciar sesión
/ip hotspot walled-garden ip add dst-address=10.20.0.162 action=accept comment="contenido local sin iniciar sesion"
# Squid solo para quien ya pasó el portal (no interfiere con la redirección al login)
/ip firewall mangle set [find comment="pbr-squid"] hotspot=auth

# --- 8.1 Firewall entre VLAN ------------------------------------------------
# ANTES de pegar este bloque: Ctrl+X en la terminal (modo seguro, <SAFE>).
# Si se corta la conexión, el MikroTik deshace los cambios solo.
# Cuando todo funcione, Ctrl+X otra vez para dejarlos guardados.
/interface list add name=LAN
/interface list add name=WAN
/interface list member add list=WAN interface=ether9
/interface list member add list=LAN interface=vlan10-admin
/interface list member add list=LAN interface=vlan20-salud
/interface list member add list=LAN interface=vlan30-publica
/ip firewall filter
# --- Al propio MikroTik ---
add chain=input connection-state=established,related action=accept comment="hub: respuestas"
add chain=input connection-state=invalid action=drop
add chain=input protocol=icmp action=accept
add chain=input in-interface=vlan10-admin protocol=tcp dst-port=22,8291 action=accept comment="hub: gestion VLAN 10"
add chain=input in-interface=ether9 src-address=10.42.0.0/24 protocol=tcp dst-port=22,8291 action=accept comment="hub: gestion portatil (solo laboratorio)"
add chain=input in-interface-list=LAN protocol=udp dst-port=53,67 action=accept comment="hub: DNS y relay DHCP"
add chain=input in-interface-list=LAN protocol=tcp dst-port=53 action=accept
add chain=input action=drop comment="hub: todo lo demas al MikroTik"
# --- Entre redes ---
add chain=forward connection-state=established,related action=accept comment="hub: respuestas"
add chain=forward connection-state=invalid action=drop
add chain=forward in-interface=vlan10-admin action=accept comment="hub: VLAN 10 sin restriccion"
add chain=forward in-interface=ether9 src-address=10.42.0.0/24 dst-address=10.20.0.0/24 action=accept comment="hub: portatil a la LAN (solo laboratorio)"
add chain=forward in-interface-list=LAN dst-address=10.20.0.162 protocol=udp dst-port=53,123 action=accept comment="hub: DNS y NTP"
add chain=forward in-interface-list=LAN dst-address=10.20.0.162 protocol=tcp dst-port=53,80,443 action=accept comment="hub: portal y CDN"
add chain=forward in-interface=vlan20-salud dst-address=10.20.0.162 protocol=tcp dst-port=8883 action=accept comment="hub: MQTT salud (Fase 3)"
add chain=forward routing-mark=to-proxy action=accept comment="hub: HTTP desviado a Squid"
add chain=forward in-interface-list=LAN out-interface-list=WAN action=accept comment="hub: salida a Internet"
add chain=forward action=drop comment="hub: todo lo demas, incluido trafico entre VLAN"
# Revisar que suban los contadores y luego Ctrl+X para salir del modo seguro
/ip firewall filter print stats

# --- 8.2 Límites de ancho de banda (valores iniciales de la Fase 1) ---------
/queue simple add name=salud target=10.20.0.128/27 limit-at=3M/10M max-limit=100M/100M priority=1/1 comment="garantizado 3/10 Mbps"
/queue simple add name=publica target=10.20.0.0/25 max-limit=5M/20M priority=8/8 comment="maximo 5/20 Mbps para todo el grupo"
/ip hotspot user profile set publica parent-queue=publica

# --- Al terminar: guardar (la contraseña del respaldo NO va al repositorio) --
# /system backup save name=hub-ccr2004-AAAA-MM-DD password=<clave del respaldo>
# /export file=hub-ccr2004-AAAA-MM-DD
