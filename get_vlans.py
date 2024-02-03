from netmiko import ConnectHandler
import net_conn
import re
from colorama import Fore
import json

class CiscoDevice:
     
    def get_device_info(self):
        with open("hosts", "r") as f:
            addresses = f.read().splitlines()
        

        for devices in addresses:
            device = {"device_type": "cisco_nxos",
                    "host": devices,
                    "username": net_conn.username,
                    "password": net_conn.passwd,
                    "secret": net_conn.passwd,
            }

            # Connect to device
            ssh_connection = ConnectHandler(**device)

        
            show_vlan = ssh_connection.find_prompt()
            show_ver_output = ssh_connection.send_command('show version')
            show_vlan = ssh_connection.send_command('show vlan', use_textfsm=True)
            
            
            hostname_pattern = r'Device.+name:.(\S+)'
            hostname = re.findall(hostname_pattern,show_ver_output)
            print(f'Hostname: {hostname}')

            vlanid_pattern = r"vlan_id':.'(\d+)"
            vlanid = re.findall(vlanid_pattern,str(show_vlan))
            print(f'Vlans ID: {vlanid}\n')

            vlanfull_pattern = r"vlan_id':.'(\d+).,.'vlan_name':.'(\S+\w)"
            vlanid_name = re.findall(vlanfull_pattern,str(show_vlan))
            print(f'Vlan and name: {vlanid_name}\n')
            
            model_pattern = r'cisco.Nexus9000.(\S+)'
            model = re.findall(model_pattern,show_ver_output)
            print(f'Model: {model}')
            
            version_pattern = r'NXOS.+version.(\S+)'
            version = re.findall(version_pattern, show_ver_output)
            print(f'NXOS Version: {version}')
            
            uptime_pattern = r'Kernel.uptime.is.(\S.*)'
            uptime = re.findall(uptime_pattern,show_ver_output)
            print(f'Uptime: {uptime}')
            
            
            print(json.dumps(show_vlan, indent = 2))
            
            #show_clock = ssh_connection.send_command('show clock')
            #print(f"Hour: {show_clock}")

sa = CiscoDevice()
sa.get_device_info()
    

    