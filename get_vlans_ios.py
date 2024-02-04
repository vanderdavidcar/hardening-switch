from netmiko import ConnectHandler
import net_conn
import re
from colorama import Fore
import json

class CiscoDeviceIOS:
     
    def get_vlans_info(self):
        with open("hosts", "r") as f:
            addresses = f.read().splitlines()
        

        for devices in addresses:
            device = {"device_type": "cisco_ios",
                    "host": devices,
                    "username": net_conn.user_lab,
                    "password": net_conn.pass_lab,
                    "secret": net_conn.pass_lab,
            }

            # Connect to device
            ssh_connection = ConnectHandler(**device)

        
            show_vlan = ssh_connection.find_prompt()
            show_ver_output = ssh_connection.send_command('show run')
            show_vlan = ssh_connection.send_command('show vlan', use_textfsm=True)
            
            hostname_pattern = r'hostname.(\S+)'
            hostname = re.findall(hostname_pattern,show_ver_output)
            
            """
            Using FORE to change line color
            """
            print(Fore.YELLOW + f'Hostname: {hostname}' + Fore.RESET)

            vlanid_pattern = r"vlan_id':.'(\d+)"
            vlanid = re.findall(vlanid_pattern,str(show_vlan))
            print(f'\nVlans ID: {vlanid}')

            vlanfull_pattern = r"vlan_id':.'(\d+).,.'name':.'(\S+\w)"
            vlanid_name = re.findall(vlanfull_pattern,str(show_vlan))
            print(f'Vlan and name: {vlanid_name}\n')            
            
            #print(json.dumps(show_vlan, indent = 2))
            
            #show_clock = ssh_connection.send_command('show clock')
            #print(f"Hour: {show_clock}")

sa = CiscoDeviceIOS()
sa.get_vlans_info()
    

    