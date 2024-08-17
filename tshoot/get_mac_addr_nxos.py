from netmiko import ConnectHandler
from dotenv import load_dotenv
from datetime import datetime
import re
import net_conn
load_dotenv()

start_time = datetime.now()

devices = ["brlp-spac08-repl2-1"]

# Vlan range used for loop
vlan = range(372,375)

def get_mac_addr_nxos():
    for ip in devices:
        
        # Netmiko connection
        iosv = net_conn.netmiko_dellos9(ip)
        print(f"\n{'#'*79}\nConnecting to the device: {ip}\n")
        net_connect = ConnectHandler(**iosv)
        
        # Loop 
        for vlans in vlan:
            
            print("+"*40)
            print(f"\nVlan ID {vlans}")
            show_mac_add = net_connect.send_command(f'show mac address vlan {vlans}')

            # Regex pattern to find out all mac-addresses
            mac_add_pattern = "(?:[0-9A-Fa-f]{4}[.-])+.{4}"
            mac_add_regex = re.findall(mac_add_pattern,show_mac_add)
            
            # Condition after find mac-addresses
            if mac_add_regex:
                print(f"{show_mac_add}\n")
            else:
                print(f"Without mac-addresses")

        
        end_time = datetime.now()
        print("Total time: {}".format(end_time - start_time))

get_mac_addr_nxos()