from netmiko import ConnectHandler
import net_conn
import re


with open("ip_list.txt") as f:
    hosts = f.read().splitlines()

class CiscoDevice:
        def __init__(self):
            self.connection = ConnectHandler(ip='S3',
                                            username=net_conn.user_lab, 
                                            password=net_conn.pass_lab,
                                            device_type="cisco_ios")
    
        def get_version(self):
            show_ver_output = self.connection.find_prompt()
            show_ver_output += self.connection.send_command('show version')
            version_pattern = re.compile(r'Cisco.+Version.(\d...)')
            version = re.findall(version_pattern, show_ver_output)
            print(f'IOS Version: {version}')

        def hostname(self):
            sh_run_output = self.connection.find_prompt()
            sh_run_output += self.connection.send_command('show run')
            hostname_pattern = re.compile(r'hostname (\S+)')
            hostname = re.findall(hostname_pattern,sh_run_output)
            print(f'Hostname: {hostname}')

sa = CiscoDevice()
sa.hostname()
sa.get_version()