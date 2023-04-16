from netmiko import ConnectHandler
import re
import net_conn
import auth
import logging

# To show logging and troubleshooting in case of problems
logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

"""
The main proposal here is to identify all interfaces on environment without that not using 
and disable to avoid man-in-the-middle.
I'm using Netbox as Source of Truth to connect in devices. Function net_conn imported to use Netmiko 
and function auth to pass all the parameters to authenticate 
"""
#nb_api = list(auth.nb.dcim.devices.filter("mgmt",model="9200"))
nb_api = list(auth.nb.dcim.devices.filter(platform="cisco-ios"))
#nb_api = list(auth.nb.dcim.devices.filter(platform="cisco-nx-os"))
#nb_api = list(auth.nb.dcim.devices.filter(platform="dellos"))
print(f'All devices will be check:\n{nb_api}\n')

# Regex pattern to find all kinds of interface like FastEthernet, GigabitEthernet, Ethernet, TenGigabiEthernet and so on..
int_pattern = re.compile(r"(?P<interface>\S+[A-Za-z][0-9].[0-9].[0-9]*)")

"""
Loop devices find on Netbox
"""
def errdisabled():
    for ip in nb_api:
        ipadd = str(ip)
        ios = net_conn.netmiko_lab(ipadd)
        print(f"Connecting to {ipadd}")
        net_connect = ConnectHandler(**ios)
        output = net_connect.send_command('show interface status | in err-disable')
        match = int_pattern.search(output)
        try:
            interface = match.group("interface")
            all_int = re.findall(int_pattern, output)
        except (AttributeError):
            print('No such attribute')
            continue
        #if "err-disable" in output:
        if "err-disable" in output:
            print(f'\nInterfaces in err-disable status:\n{all_int}\n')
    
        for i in all_int:
            #Turn on err-disabled interfaces
            cmd = net_connect.send_config_set([f'interface {i}', 'shutdown', 'no shutdown'])
            print(cmd)
errdisabled()

