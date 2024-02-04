from netmiko import ConnectHandler
import net_conn
import re
from colorama import Fore

class CiscoDevice:
     
    def get_device_info(self):
        with open("hosts", "r") as f:
            addresses = f.read().splitlines()
        

        for devices in addresses:
            device = {"device_type": "cisco_nxos",
                    "host": devices,
                    "username": net_conn.user_lab,
                    "password": net_conn.pass_lab,
                    "secret": net_conn.pass_lab,
            }

            # Connect to device
            ssh_connection = ConnectHandler(**device)

        
            show_ver_output = ssh_connection.find_prompt()
            show_ver_output = ssh_connection.send_command('show version')
            
            hostname_pattern = r'Device.+name:.(\S+)'
            hostname = re.findall(hostname_pattern,show_ver_output)
            print(f'Hostname: {hostname}')
            
            model_pattern = r'cisco.Nexus9000.(\S+)'
            model = re.findall(model_pattern,show_ver_output)
            print(f'Model: {model}')
            
            version_pattern = r'NXOS.+version.(\S+)'
            version = re.findall(version_pattern, show_ver_output)
            print(f'NXOS Version: {version}')
            
            uptime_pattern = r'Kernel.uptime.is.(\S.*)'
            uptime = re.findall(uptime_pattern,show_ver_output)
            print(f'Uptime: {uptime}')
            
            show_clock = ssh_connection.send_command('show clock')
            print(f"Hour: {show_clock}")

sa = CiscoDevice()
sa.get_device_info()
    

    