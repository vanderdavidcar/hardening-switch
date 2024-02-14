import threading
import net_conn
from netmiko import ConnectHandler
from datetime import datetime
from colorama import Fore

start_time = datetime.now()
end_time = datetime.now()

with open("hosts") as f:
    address = f.read().splitlines()


def cisco_cmd():
    for host in address:
        my_dictionay = {
            "ip": host,
            "username": net_conn.user_lab,
            "password": net_conn.pass_lab,
            "device_type": "cisco_ios",
        }

        print(
            Fore.LIGHTBLACK_EX
            + f"\nConnecting to the device {host} {'#'*10}"
            + Fore.RESET
        )
        ssh_connection = ConnectHandler(**my_dictionay)
        show_ver_output = ssh_connection.find_prompt()
        show_ver_output = ssh_connection.send_command("show version", use_genie=True)
        #print(show_ver_output)

if __name__ == "__main__":
    cisco_cmd()    
    show_version_thread = []
    for i in address:
        print(i)
        print()
        show_thread = threading.Thread(target=cisco_cmd, kwargs=i)
        show_thread.start()
        show_version_thread.append(show_thread)
        show_thread.join()




endtime = end_time - start_time
print(endtime)
