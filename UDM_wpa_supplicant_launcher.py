import spur
import os
from requests import get
import time
import datetime

ip_check = '' # set to prefix of WAN IP i.e = '164' (you can enter the entire IP if you have a static WAN)
ping_host = 'ping.ui.com' # set host to ping - only used if ip_check is not provided

net_check = 1 # in minutes - how often to check ip address or ping to determine if network is down
ssh_internval = 5 # in minutes - only allow ssh session when network is down once every 5 minutes

udm_creds = {
    'hostname' : '',        # UDM IP Address (i.e 10.0.1.1)
    'username' : 'root',    # UDM SSH Username
    'password' : ''         # UDM SSH  Password
}


def main_loop():
    last_ssh_time = 0
    while True:
        network_down = False
        if ip_check and not verify_ip():
            network_down = True
        elif ping_host and not ping():
            network_down = True
        if network_down:
            print(str(datetime.datetime.now()) + ":  network is down")
            if (time.time() - last_ssh_time) >= ssh_internval*60:
                print(str(datetime.datetime.now()) + ": ssh(ing) into UDM")
                last_ssh_time = time.time()
                udm_ssh()
                print("---------------------------------------")
                print()
        time.sleep(net_check * 60)

def verify_ip():
    try:
        ip = get('https://api.ipify.org', timeout=6).text
    except:
        return False
    if ip.startswith(ip_check):
        return True
    return False

def ping():
    response = os.system("ping -c 3 -q " + ping_host + " >/dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False

def udm_ssh():
    try:
        with spur.SshShell(hostname=udm_creds['hostname'], username=udm_creds['username'], password=udm_creds['password'], connect_timeout=6) as shell:
            if "wpa_supplicant" in str(shell.run(["podman", "ps"]).output):
                print("wpa_supplicant is already running")
                return
            shell.run(["podman", "container", "start", "wpa_supplicant-udmpro"])
            print("Launched wpa_supplicant")
            return
    except Exception as e:
        print(e)
        return

def main():
    if not (ping_host or ip_check):
        print("Specify ping_host and/or ip_check")
        return
    if not udm_creds['hostname'] or not udm_creds['username'] or not udm_creds['password']:
        print("Enter creds in udm_creds")
        return
    print("UDM Script is Running")
    main_loop()

main()
