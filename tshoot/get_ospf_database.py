from netmiko import ConnectHandler
import net_conn
from dotenv import load_dotenv
load_dotenv()
import re
from colorama import Fore
from drawio_network_plot.drawio_network_plot import NetPlot

# List of devices
devices = ['S1']

for hosts in devices: 
        print()
        print("#" * 79)
        iosv = net_conn.netmiko_nxos(hosts)
        print(f'Connecting to device {hosts} and find all OSPF Adjacency')
    
        net_connect = ConnectHandler(**iosv)
        print()
        
        # Command to find router ID of devices
        show_routerID = net_connect.send_command('sh ip ospf database router | in Neighboring')
        
        regex = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        pattern = re.findall(regex, show_routerID)

        # remove duplicate information into list
        routerID = list(dict.fromkeys(pattern))
        print("Router IDs")
        print(f"{routerID}\n")
        net_connect.disconnect()

# New loop to connect on neighbors found on device
print("#" * 79)
for ip in routerID:
        list_of_neighborship = []

        iosv = net_conn.netmiko_nxos(ip)
        print(Fore.YELLOW + f'\nConnecting to the device: {ip}' + Fore.RESET)

        net_connect = ConnectHandler(**iosv)
        cmd = net_connect.send_command(f'sh ip ospf database router {ip} | in Neighboring')
        
        # Regex pattern to find only IP Address
        regex_cmd = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        pattern_cmd = re.findall(regex_cmd, cmd)
        
        # remove duplicate information into list
        mylist = list(dict.fromkeys(pattern_cmd))
        print(f"Router ID {ip} has neighborship with:")

        for line in mylist:
                # regex to search the name of the device before the domain ID ".default" , then removing the word ".default" from the string
                link = {
                            'sourceNodeID' : ip,
                            'destinationNodeID' : line
                            }

                list_of_neighborship.append(link)
        
        # Getting list of links for each device
        for peering in list_of_neighborship:
                print(f'{peering}')
