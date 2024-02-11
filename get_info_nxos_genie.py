from netmiko import ConnectHandler
import net_conn
from colorama import Fore

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
            print(Fore.YELLOW + f'Connecting to the device: {devices}' + Fore.RESET)
            cmd = ssh_connection.find_prompt()
            cmd = ssh_connection.send_command('show version', use_genie=True)
            

            show_ver_output = dict(cmd)
            print(f'Hostname: {show_ver_output["platform"]["hardware"]["device_name"]}')
            print(f'Model: {show_ver_output["platform"]["hardware"]["model"]}')
            print(f'NXOS Version: {show_ver_output["platform"]["software"]["system_version"]}')
            
            days = {show_ver_output["platform"]["kernel_uptime"]["days"]}
            hours = {show_ver_output["platform"]["kernel_uptime"]["hours"]}
            minutes = {show_ver_output["platform"]["kernel_uptime"]["minutes"]}
            seconds = {show_ver_output["platform"]["kernel_uptime"]["seconds"]}
            print(f'Uptime:\nDays: {days}, Hours: {hours}, Minutes: {minutes} and Seconds: {seconds}\n')
            
            
sa = CiscoDevice()
sa.get_device_info()
    

    