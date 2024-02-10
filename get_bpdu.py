from netmiko import ConnectHandler
import net_conn
import re
from colorama import Fore
import threading

class CiscoDeviceIOS:

    def get_vlans_info(self):
        with open("hosts", "r") as f:
            addresses = f.read().splitlines()

        for devices in addresses:
            print(Fore.LIGHTBLACK_EX + f"\nConnecting to device: {devices}\n" + Fore.RESET)
            device = {
                "device_type": "cisco_ios",
                "host": devices,
                "username": net_conn.user_lab,
                "password": net_conn.pass_lab,
                "secret": net_conn.pass_lab,
            }

            # Connect to device
            ssh_connection = ConnectHandler(**device)

            show_vlan = ssh_connection.find_prompt()
            #show_ver_output = ssh_connection.send_command("show run")
            show_bpdu = ssh_connection.send_command("show spanning-tree detail | inc Eth|BPDU")
            #print(show_bpdu)

            bpdu_pattern = r"Port.\w..(\S+[A-Za-z][0-9].[0-9].[0-9]*).+\s+BPDU:.sent.\w+,.received.(\d+)"
            bpdu = re.findall(bpdu_pattern, show_bpdu)
            
            print(bpdu)
            
sa = CiscoDeviceIOS()
sa.get_vlans_info()
