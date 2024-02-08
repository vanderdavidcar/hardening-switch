import threading
from netmiko import ConnectHandler
import net_conn

with open("hosts", "r") as f:
    device = f.read().splitlines()

def connect_to_dev(device):
    device_connect = ConnectHandler(**device)
    output = device_connect.send_command("show arp")
    print(output)


processes = []
for devices in device:
    p = threading.Thread(target=connect_to_dev, args=(device,))
    processes.append(p)
    p.start()

for proc in processes:
    p.join()