from netmiko import ConnectHandler
import net_conn
import re
from colorama import Fore

class CiscoDeviceIOS:
     
    def get_device_info(self):
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

        
            show_ver_output = ssh_connection.find_prompt()
            show_ver_output = ssh_connection.send_command('show version')

            hostname_pattern = r'(\S+).+uptime.is'
            hostname = re.findall(hostname_pattern,show_ver_output)
            print(Fore.YELLOW+f'\nHostname: {hostname}'+Fore.RESET)
            
            version_pattern = r'Version.(\d+..)'
            version = re.findall(version_pattern, show_ver_output)
            print(f'IOS Version: {version}')
            
            uptime_pattern = r'uptime.is.(\S.+)'
            uptime = re.findall(uptime_pattern,show_ver_output)
            print(f'Uptime: {uptime}')
            
            show_clock = ssh_connection.send_command('show clock')
            print(f"Hour: {show_clock}")

sa = CiscoDeviceIOS()
sa.get_device_info()
    

    