
lan_template1 = """config interface 'lan{}'                    
        option ifname 'eth1.{}'                       
        option proto 'static'"""

lan_template2 = """config interface 'lan{}'                    
        option ifname 'eth1.{}'                       
        option proto 'static'"""
force_template1 = """config interface 'lan{}'
	option ifname 'eth1.{}'
option force_link '1'
	option proto 'static'
	option netmask '255.255.255.0'
	option ip6assign '60'
	option ipaddr '{}'
"""

force_template2 = """config interface 'lan{}'
	option ifname 'eth1.{}'
option force_link '1'
	option proto 'static'
	option netmask '255.255.255.0'
	option ip6assign '60'
	option ipaddr '{}'
"""


network_template = """config interface 'loopback'
	option ifname 'lo'
	option proto 'static'
	option ipaddr '127.0.0.1'
	option netmask '255.0.0.0'

config interface 'wan'
        option ifname 'eth0'
        option proto 'dhcp'

config switch
        option name 'switch0'
        option reset '1'
        option enable_vlan '1'
        option enable_learning '0'

config switch_vlan
        option vlan '1'
        option ports '2 0t'
        option device 'switch0'

config switch_vlan
        option vlan '2'
        option ports '3 0t'
        option device 'switch0'

config switch_vlan
        option vlan '3'
        option ports '4 0t'
        option device 'switch0'

config switch_vlan
        option vlan '4'
        option ports '5 0t' #For the TPLink1750
        option device 'switch0'

# The next 4 lines are not necessary for the Netgear R6100
config switch_vlan
        option vlan '5'
        option ports '1 6'
        option device 'switch0'

# eth1.* should be static and controlled by the controller

{}

{}            

{}

{}"""