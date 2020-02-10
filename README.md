# UDM "wpa_supplicant" container Launcher
Python script that ssh(es) into a UDM(P) if a network outages occurs and launches the "wpa_supplicant" container if it is not already running.

# Features
User can specify what determines a network outage (i.e based on WAN IP or ping failure) prior to the ssh session which checks to see if the container is already running (and launches it if isn't). 

# Installation
1. pip3 install spur
2. Download the "UDM_wpa_supplicant_launcher.py" file 

# Usage
On the "UDM_wpa_supplicant_launcher.py" file
"ip_check"/"ping_host" are used to determine if the network is down. 
* ip_check = '' - set to prefix of WAN IP i.e = '164' (you can enter the entire IP if you have a static WAN). This is useful if you are using WAN Failover so you can determine if you are on AT&T or the failover network. 
* ping_host = 'ping.ui.com' # set host to ping - only used if ip_check is not provided. 
