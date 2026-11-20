# 2026-11-19 18:01:07 by RouterOS 7.13.5
# software id = WDCW-PNZP
#
# model = CCR2004-16G-2S+
# serial number = HGA09ZBSP3T
/interface bridge
add name=br-lan vlan-filtering=yes
/interface ethernet
set [ find default-name=ether1 ] disabled=yes
set [ find default-name=ether2 ] disabled=yes
set [ find default-name=ether3 ] disabled=yes
set [ find default-name=ether4 ] disabled=yes
set [ find default-name=ether5 ] disabled=yes
set [ find default-name=ether6 ] disabled=yes
set [ find default-name=ether7 ] disabled=yes
set [ find default-name=ether8 ] disabled=yes
set [ find default-name=ether9 ] comment="WAN: portatil (simula Starlink)"
set [ find default-name=ether10 ] comment=\
    "Servidor hub Raspberry Pi (VLAN 10)"
set [ find default-name=ether11 ] comment="AP UniFi (troncal VLAN 10/20/30)"
set [ find default-name=ether12 ] comment="Portatil admin (VLAN 10)"
set [ find default-name=ether13 ] disabled=yes
set [ find default-name=ether14 ] disabled=yes
set [ find default-name=ether15 ] disabled=yes
set [ find default-name=ether16 ] disabled=yes
set [ find default-name=sfp-sfpplus1 ] disabled=yes
set [ find default-name=sfp-sfpplus2 ] disabled=yes
/interface vlan
add interface=br-lan name=vlan10-admin vlan-id=10
add interface=br-lan name=vlan20-salud vlan-id=20
add interface=br-lan name=vlan30-publica vlan-id=30
/interface ethernet switch port-isolation
set 0 !forwarding-override
set 1 !forwarding-override
set 2 !forwarding-override
set 3 !forwarding-override
set 4 !forwarding-override
set 5 !forwarding-override
set 6 !forwarding-override
set 7 !forwarding-override
set 16 !forwarding-override
/interface list
add name=LAN
add name=WAN
/ip hotspot profile
add dns-name=wifi-salud.hub.lan hotspot-address=10.20.0.129 login-by=https \
    name=hs-salud ssl-certificate=hub.crt_0
/ip hotspot
add disabled=no interface=vlan20-salud name=hotspot-salud profile=hs-salud
/ip hotspot user profile
add name=salud session-timeout=8h shared-users=2
/port
set 0 name=serial0
set 1 name=serial1
/queue simple
add comment="garantizado 3/10 Mbps" limit-at=3M/10M max-limit=100M/100M name=\
    salud priority=1/1 target=10.20.0.128/27
add comment="maximo 5/20 Mbps para todo el grupo" max-limit=5M/20M name=\
    publica target=10.20.0.0/25
/ip hotspot user profile
add name=publica parent-queue=publica rate-limit=1M/2M session-timeout=2h
/ip hotspot profile
add dns-name=wifi-publica.hub.lan hotspot-address=10.20.0.1 login-by=\
    https,trial name=hs-publica ssl-certificate=hub.crt_0 trial-uptime-limit=\
    2h trial-user-profile=publica
/ip hotspot
add disabled=no interface=vlan30-publica name=hotspot-publica profile=\
    hs-publica
/routing table
add fib name=to-proxy
/interface bridge port
add bridge=br-lan interface=ether10 pvid=10
add bridge=br-lan interface=ether11 pvid=10
add bridge=br-lan interface=ether12 pvid=10
/interface bridge vlan
add bridge=br-lan tagged=br-lan untagged=ether10,ether11,ether12 vlan-ids=10
add bridge=br-lan tagged=br-lan,ether11 vlan-ids=20
add bridge=br-lan tagged=br-lan,ether11 vlan-ids=30
/interface list member
add interface=ether9 list=WAN
add interface=vlan10-admin list=LAN
add interface=vlan20-salud list=LAN
add interface=vlan30-publica list=LAN
/ip address
add address=10.20.0.161/28 interface=vlan10-admin network=10.20.0.160
add address=10.20.0.129/27 interface=vlan20-salud network=10.20.0.128
add address=10.20.0.1/25 interface=vlan30-publica network=10.20.0.0
/ip dhcp-client
add interface=ether9
/ip dhcp-relay
add dhcp-server=10.20.0.162 disabled=no interface=vlan20-salud local-address=\
    10.20.0.129 name=relay-salud
add dhcp-server=10.20.0.162 disabled=no interface=vlan30-publica \
    local-address=10.20.0.1 name=relay-publica
/ip dns
set allow-remote-requests=yes servers=10.20.0.162
/ip firewall address-list
add address=10.20.0.0/25 comment="VLAN 30 publica" list=clientes-proxy
add address=10.20.0.128/27 comment="VLAN 20 salud" list=clientes-proxy
/ip firewall filter
add action=passthrough chain=unused-hs-chain comment=\
    "place hotspot rules here" disabled=yes
add action=accept chain=input comment="hub: respuestas" connection-state=\
    established,related
add action=drop chain=input comment="hub: invalidos" connection-state=invalid
add action=accept chain=input comment="hub: ping" protocol=icmp
add action=accept chain=input comment="hub: gestion VLAN 10" dst-port=22,8291 \
    in-interface=vlan10-admin protocol=tcp
add action=accept chain=input comment=\
    "hub: gestion portatil (solo laboratorio)" dst-port=22,8291 in-interface=\
    ether9 protocol=tcp src-address=10.42.0.0/24
add action=accept chain=input comment="hub: DNS y relay DHCP" dst-port=53,67 \
    in-interface-list=LAN protocol=udp
add action=accept chain=input comment="hub: DNS por TCP" dst-port=53 \
    in-interface-list=LAN protocol=tcp
add action=drop chain=input comment="hub: todo lo demas al MikroTik"
add action=accept chain=forward comment="hub: respuestas" connection-state=\
    established,related
add action=drop chain=forward comment="hub: invalidos" connection-state=\
    invalid
add action=accept chain=forward comment="hub: VLAN 10 sin restriccion" \
    in-interface=vlan10-admin
add action=accept chain=forward comment=\
    "hub: portatil a la LAN (solo laboratorio)" dst-address=10.20.0.0/24 \
    in-interface=ether9 src-address=10.42.0.0/24
add action=accept chain=forward comment="hub: DNS y NTP" dst-address=\
    10.20.0.162 dst-port=53,123 in-interface-list=LAN protocol=udp
add action=accept chain=forward comment="hub: portal y CDN" dst-address=\
    10.20.0.162 dst-port=53,80,443 in-interface-list=LAN protocol=tcp
add action=accept chain=forward comment="hub: MQTT salud (Fase 3)" \
    dst-address=10.20.0.162 dst-port=8883 in-interface=vlan20-salud protocol=\
    tcp
add action=accept chain=forward comment="hub: HTTP desviado a Squid" \
    routing-mark=to-proxy
add action=accept chain=forward comment="hub: salida a Internet" \
    in-interface-list=LAN out-interface-list=WAN
add action=drop chain=forward comment=\
    "hub: todo lo demas, incluido trafico entre VLAN"
/ip firewall mangle
add action=mark-routing chain=prerouting comment=pbr-squid dst-address=\
    !10.20.0.0/24 dst-port=80 hotspot=auth new-routing-mark=to-proxy \
    passthrough=no protocol=tcp src-address-list=clientes-proxy
/ip firewall nat
add action=passthrough chain=unused-hs-chain comment=\
    "place hotspot rules here" disabled=yes
add action=masquerade chain=srcnat comment=\
    "NAT del sitio (resumen 10.20.0.0/24)" out-interface=ether9 src-address=\
    10.20.0.0/24
add action=masquerade chain=srcnat comment="lab: portatil a la web del AP" \
    dst-address=10.20.0.163 src-address=10.42.0.0/24
/ip hotspot user
add name=enfermera01 profile=salud server=hotspot-salud
add name=promotor01 profile=salud server=hotspot-salud
/ip hotspot walled-garden
add comment="place hotspot rules here" disabled=yes
/ip hotspot walled-garden ip
add action=accept comment="contenido local sin iniciar sesion" disabled=no \
    dst-address=10.20.0.162
/ip route
add check-gateway=ping comment="PBR hacia Squid" dst-address=0.0.0.0/0 \
    gateway=10.20.0.162 routing-table=to-proxy
/ip service
set telnet disabled=yes
set ftp disabled=yes
set api disabled=yes
set api-ssl disabled=yes
/system clock
set time-zone-name=America/Bogota
/system identity
set name=hub-mikrotik
/system note
set show-at-login=no
/system ntp client
set enabled=yes
/system ntp client servers
add address=10.20.0.162
/system routerboard settings
set enter-setup-on=delete-key
/tool netwatch
add comment="vigila Squid" down-script=\
    "/ip firewall mangle disable [find comment=\"pbr-squid\"]" host=\
    10.20.0.162 interval=10s port=3129 type=tcp-conn up-script=\
    "/ip firewall mangle enable [find comment=\"pbr-squid\"]"
