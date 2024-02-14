# https://www.consentfactory.com/python-threading-queuing-netmiko/

# Queuing and threading libraries
from queue import Queue
import threading

# Import function with username and password
from net_conn import user_lab, pass_lab

# Importing Netmiko modules
from netmiko import ConnectHandler
from datetime import datetime
from colorama import Fore

start_time = datetime.now()
end_time = datetime.now()
# Set up thread count for number of threads to spin up
num_threads = 8
# This sets up the queue
enclosure_queue = Queue()
# Set up thread lock so that only one thread prints at a time
print_lock = threading.Lock()


with open("hosts") as f:
    address = f.read().splitlines()

command = "show version"


def deviceconnector(i, q):

    while True:

        # These print statements are largely for the user indicating where the process is at
        # and aren't required
        print("{}: Waiting for IP address...".format(i))
        ip = q.get()
        print("\n{}: Acquired IP: {}".format(i, ip))

        device_dict = {
            "host": ip,
            "username": user_lab,
            "password": pass_lab,
            "device_type": "cisco_ios",
        }

        ssh_connection = ConnectHandler(**device_dict)
        show_ver_output = ssh_connection.find_prompt()
        show_ver_output = ssh_connection.send_command(command, use_genie=True)

        with print_lock:
            print("\n{}: Printing output... {}".format(i, ip))
            print(
                Fore.LIGHTBLACK_EX
                + f"Connecting to the device {ip} {'#'*10}"
                + Fore.RESET
            )
            print(show_ver_output)

        # Set the queue task as complete, thereby removing it from the queue indefinitely
        q.task_done()


def main():

    # Setting up threads based on number set above
    for i in range(num_threads):
        # Create the thread using 'deviceconnector' as the function, passing in
        # the thread number and queue object as parameters
        thread = threading.Thread(
            target=deviceconnector,
            args=(
                i,
                enclosure_queue,
            ),
        )
        # Set the thread as a background daemon/job
        thread.setDaemon(True)
        # Start the thread
        thread.start()

    # For each ip address in "ip_addrs", add that IP address to the queue
    for ip_addr in address:
        enclosure_queue.put(ip_addr)

    # Wait for all tasks in the queue to be marked as completed (task_done)
    enclosure_queue.join()
    print("*** Script complete")


if __name__ == "__main__":

    # Calling the main function
    main()

    endtime = end_time - start_time
    print(f"\n{endtime}")
