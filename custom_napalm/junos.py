from napalm.junos.junos import JunOSDriver
from .junos_views import junos_views

import re


class CustomJunosDriver(JunOSDriver):

    def custom_local_route_table(self):
        local_route_table = junos_views.custom_local_route_table(self.device).get()
        return [ dict(local_route) for local_route in local_route_table ]


    def custom_interface_address_table(self):
        interface_address_table = junos_views.custom_interface_address_table(self.device).get()
        return [ dict(interface_address) for interface_address in interface_address_table ]


    def custom_logical_interfaces_table(self):
        logical_interfaces_table = junos_views.custom_logical_interfaces_table(self.device).get()
        return [ dict(interface) for interface in logical_interfaces_table ]


    def custom_physical_interfaces_table(self):
        physical_interfaces_table = junos_views.custom_physical_interfaces_table(self.device).get()
        return [ dict(interface) for interface in physical_interfaces_table ]


    def custom_detailed_transceiver_table(self):
        # Create a detailed interface table, combining data from the physical_interfaces_table, 
        # the custom_transceiver_table and the custom_pic_details_table
        transceiver_table = self.custom_transceiver_table()
        pic_details_table =  { 
            # create a table of all details retrieved from all 
            # 'pic_details_tables' with 'if_suffix' as the key
            pic.pop('if_suffix'):pic 
            for fpc in [
                # get pic table for each fpc/pic tuple 
                # found below in transceiver table
                self.custom_pic_details_table(fpc_slot=fpc, pic_slot=pic)
                for fpc, pic in sorted(
                    {
                        # if_suffix '1/2/3' -> (fpc, pic, port)
                        # so if_suffix '1/2/3' -> (fpc, pic (1,2)
                        ( transceiver['if_suffix'].split('/')[0], transceiver['if_suffix'].split('/')[1] )
                        for transceiver in transceiver_table 
                    }
                )
            ]
            for pic in fpc
        }
        combined_table = { 
            # join each entry in the transceiver table with a matching 
            # entry from the pic_details_table. Match on 'if_suffix'
            transceiver['if_suffix']: { **transceiver, **pic_details_table[transceiver['if_suffix']] }
            for transceiver in transceiver_table
        }
        return [ 
            # join each entry in the interfaces table with a matching 
            # entry from the transceiver table. Match on 'if_suffix' 
            # and the part of 'physical_interface' after the dash
            { **interface, **combined_table[if_prefix] }
            for interface in self.custom_physical_interfaces_table()
            if (if_prefix := interface.get('physical_interface', '').rsplit('-')[-1]) in pic_details_table
        ]


    def custom_transceiver_table(self):
        def make_table_rows(k,v):
            fpc, pic, port = k
            fpc = fpc.removeprefix('FPC ')
            pic = pic.removeprefix('PIC ')
            port = port.removeprefix('Xcvr ')
            if_name = f"{fpc}/{pic}/{port}"
            return {'if_suffix': if_name, **dict(v)}
        transceiver_table = junos_views.custom_transceiver_table(self.device).get()
        return [ make_table_rows(keys, data) for keys, data in transceiver_table.items() ]


    def custom_pic_details_table(self, fpc_slot=0, pic_slot=0):
        def make_table_rows(k,v):
            fpc, pic, port = k
            if_name = f"{fpc}/{pic}/{port}"
            return {'if_suffix': if_name, **dict(v)}
        fpc_slot = str(fpc_slot)
        pic_slot = str(pic_slot)
        pic_table = junos_views.custom_pic_details_table(self.device).get(fpc_slot=fpc_slot, pic_slot=pic_slot)
        return [ make_table_rows(keys, data) for keys, data in pic_table.items() ]


    def custom_lacp_table(self):
        lacp_table = junos_views.custom_lacp_table(self.device).get()
        return [ dict(lacp_data) for lacp_data in lacp_table ]


    def custom_vlans_table(self):
        vlan_table = junos_views.custom_vlans_table(self.device).get()
        return [ dict(vlan) for vlan in vlan_table ]


    def custom_communities_table(self):
        communities_table = junos_views.custom_communities_table(self.device).get()
        return [ dict(community_name) for community_name in communities_table ]


    def custom_prefix_lists_table(self):
        prefix_lists_table = junos_views.custom_prefix_lists_table(self.device).get()
        return [ dict(prefix_list) for prefix_list in prefix_lists_table ]


    def custom_routing_instances_table(self):
        routing_instances_table = junos_views.custom_routing_instances_table(self.device).get()
        return [ dict(routing_instance) for routing_instance in routing_instances_table ]


    def custom_routing_instances_neighbors_table(self):
        routing_instances_neighbors_table = junos_views.custom_routing_instances_neighbors_table(self.device).get()
        return [ dict(neighbor) for neighbor in routing_instances_neighbors_table ]


    def custom_route_table_raw(self):
        route_table = junos_views.custom_route_table(self.device).get()
        return [ dict(route) for route in route_table]


    def custom_route_table(self):
        raw_route_table = junos_views.custom_route_table(self.device).get()
        route_table = []
        for raw_route in raw_route_table:
            route=dict(raw_route)
            is_ip_route_table = re.match(r'(.*\.)?inet(6)?.0', route['routing_table'])
            is_selected_next_hop = route.pop('selected_next_hop') == True
            if is_ip_route_table and is_selected_next_hop:
                route_table.append(route)
        return route_table

 