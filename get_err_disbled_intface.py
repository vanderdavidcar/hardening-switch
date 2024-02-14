from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import re
import net_conn
import auth
import logging
from colorama import Fore

# To show logging and troubleshooting in case of problems
logging.basicConfig(filename="netmiko_global.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

"""
The main proposal here is to identify all interfaces on environment without that not using 
and disable to avoid man-in-the-middle.

I'm using Netbox as Source of Truth to connect in devices. Function net_conn imported to use Netmiko 
and function auth to pass all the parameters to authenticate 
"""
# nb_api = list(auth.nb.dcim.devices.filter("mgmt", model="9200"))
with open("hosts", "r") as f:
    nb_api = f.read().splitlines()


"""
Loop devices find on Netbox
"""
for ip in nb_api:
    ipadd = str(ip)
    ios = net_conn.netmiko_connection(ipadd)
    print(Fore.BLUE + f"Connecting to the device: {ipadd}" + Fore.RESET)

    """
    Handle device not reachable exceptions in Netmiko
    """
    try:
        net_connect = ConnectHandler(**ios)
    except NetmikoTimeoutException:
        print(f"Timeout to device: {ipadd}")
        continue
    except AuthenticationException:
        print(f"Authentication failure: {ipadd}")
        continue
    except EOFError:
        print(f"End of file while attempting device {ipadd}")
        continue
    except SSHException:
        print(f"SSH Issue. Are you sure SSH is enabled? {ipadd}")
        continue
    except Exception as unknown_error:
        print(f"Some other error: {str(unknown_error)}")
        continue

    # Types of devices
    list_versions = ["NX-OS", "IOS"]

    # Check software versions
    for software_ver in list_versions:
        print("Checking for " + software_ver)
        output_version = net_connect.send_command("show version")
        int_version = 0  # Reset integer value
        int_version = output_version.find(software_ver)  # Check software version
        if int_version > 0:
            print(f"Software version found: {software_ver}")
            break
        else:
            print(f"Did not find {software_ver}")

    if software_ver == "NX-OS":
        print(f"Running {software_ver} commands\n")
        output = net_connect.send_command("show interface status | in xcvrAbsen")
    elif software_ver == "IOS":
        print(f"Running {software_ver} commands\n")
        output = net_connect.send_command("show interface | in disabled")
        print(output)

    """
    Regex pattern from NXOS
    """
    # Regex to match with all kinds of interfaces
    int_pattern = re.compile(r"(?P<interface>\S+[A-Za-z][0-9].[0-9].[0-9]*)")

    """
    Handle exception when does not have a specific match 
    """
    try:
        match = int_pattern.search(output)
        interface = match.group("interface")
    except AttributeError:
        print('No such attribute "notconnect interfaces"')
        continue

    # Regex pattern
    all_int = re.findall(int_pattern, output)

    """
    Loop to print all condition interfaces
    """
    for int in all_int:
        print(Fore.RED + f"Interface founded: {int}" + Fore.RESET)

        """
        Device Hardening - Put all interfaces match with "notconnect (IOS) or xcvrAbsent (NXOS)" and put description LIVRE
        """
        config = net_connect.send_config_set(
            [f"interface {int}", "shutdwon", "no shutdown"]
        )
        print(config)
        print(Fore.YELLOW+f"\nInterface Status" + Fore.RESET)

        show_intface = net_connect.send_command(f"show interface {int} status")
        print(f"{show_intface}\n")
