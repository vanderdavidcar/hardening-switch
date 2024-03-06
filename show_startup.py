from netmiko import ConnectHandler
from getpass import getpass
import net_conn
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import re
from colorama import Fore
#start_time = datetime.now()
 

devices = open("devices_nxos.txt")

for hosts in devices: 
        print()
        print("#" * 79)
        iosv = net_conn.netmiko_nxos(hosts)
        print('Connecting to device:  ' + hosts)
    
        net_connect = ConnectHandler(**iosv)
        print()
        show_startup = net_connect.send_command('show startup-config')
        show_version = net_connect.send_command('show version', use_genie=True)

        pattern_statup = 'Startup.(\S+.+)'
        regex_startup = re.findall(pattern_statup, show_startup)
        if regex_startup:
                print(regex_startup)
                print(f"Uptime: {show_version['platform']['kernel_uptime']}")
        else:
                print(Fore.RED + f"No startup-config" + Fore.RESET)
                print(f"Uptime: {show_version['platform']['kernel_uptime']}")