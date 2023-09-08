from napalm import get_network_driver
from custom_napalm.junos_views import junos_views
from lib.helpers.secrets import USERNAME, PASSWORD
from rich import print
junos_driver = get_network_driver('junos')
device = junos_driver(hostname='br1.gs.network.is.nl', username=USERNAME, password=PASSWORD, timeout=900)
device.open()

#print('custom_detailed_interfaces_table')
#p = device.custom_detailed_interfaces_table()

#print('custom_logical_interfaces_table')
#l = device.custom_logical_interfaces_table()

#print('custom_physical_interfaces_table')
#k = device.custom_physical_interfaces_table()



#print('custom_direct_route_table')
#o = device.custom_direct_route_table()

#print('custom_local_route_table')
#n = device.custom_local_route_table()


print('custom_interface_address_table')
m = device.custom_interface_address_table()

#print('custom_logical_interfaces_table')
#l = device.custom_logical_interfaces_table()

#print('custom_physical_interfaces_table')
#k = device.custom_physical_interfaces_table()

#print('custom_transceiver_table')
#j = device.custom_transceiver_table()

#print('custom_pic_details_table')
#i = device.custom_pic_details_table(fpc_slot=0, pic_slot=0)

#print('custom_lacp_table')
#h = device.custom_lacp_table()

#print('custom_vlans_table')
#g = device.custom_vlans_table()

#print('custom_communities_table')
#f = device.custom_communities_table()

#print('custom_prefix_lists_table')
#e = device.custom_prefix_lists_table()

#print('custom_routing_instances_table')
#d = device.custom_routing_instances_table()

#print('custom_routing_instances_neighbors_table')
#c = device.custom_routing_instances_neighbors_table()

#print('custom_route_table')
#b = device.custom_route_table()

