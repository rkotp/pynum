# **************************************************************************************
# **************************************************************************************
# IMPORTS
import random
import string
import multiprocessing
from .print_options import *
import random
from scapy.all import *
from termcolor import colored
import subprocess
import os
from .interfaces import *
import ipaddress
import lib.wifi_arp_spoofing as arps
import lib.wireless_active_scanner as was
import lib.get_debug as lgd
import lib.log as liblog
#import slow_connection
# TO_DO: CHANGE FORMAT OF IMPORTS

# **************************************************************************************
# **************************************************************************************
# INITIALIZING THE OBJECTS AND PARAMETERS

queue = multiprocessing.Queue()
ifaces = []
detected_hosts = []
passive_sniffers = []
active_processes = []
cli = True 
wui = False
debug_mode = lgd.get_dbg()[1]

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO SELECT ONE INTERFACE IF NEEDED 

def select_interface(interfaces):

	# IF IT ONLY EXISTS ONE INTERFACE OR THERE IS NOT INTERFACES, IT SHOULD NOT ASK FOR IT
	if (len(interfaces)==1):
		return interfaces[0]
	elif(len(interfaces)==0):
		return None

	# IN THE OTHER CASES
	else:
		i = 1
		# INTERFACES WILL BE PRINTED WIH AN IDENTIFIER
		print("\nSeveral interfaces found")
		for interface in interfaces:
			print(str(i) + " -->  " + ifaces[i-1])
			i = i + 1
		
		# AND THE IDENTIFIER OF THE SELECTED INTERFACE WILL BE ASKED AND VALIDATED BEFORE RETURNING THE SELECTED
		print("\nSelect the interface to work with. Type the index of the interface:\n>>> ",end="")
		iface_index = input()
		try:
			val = int(iface_index)
			if not(val > 0 and val <= len(ifaces)):
				print("You should enter the index corresponding the option you want. Please, re-run it properly")
			else:
				iface = ifaces[val-1]
				print("\nInterface selected: " + colored(iface, 'green',attrs=['bold']))
				return iface
		except ValueError:
			print("You should enter the index corresponding the option you want. Please, re-run it properly")
			return None

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO GET THE NETWORK GIVEN THE IP AND THE NETMASK 

def __select_host(hosts):
	if(len(hosts)<1):
		return None
	if(len(hosts)==1):
		return hosts[0]
	if(len(hosts)>1):
		print(colored("[*] Select host. Type the index of the host you want to slow down the connection:","blue"))
		aux = 1
		for host in hosts:
			print(colored("[*][" + str(aux) + "] " + host[0],"blue"))
			aux = aux + 1
		
		host_index = input()
		try:
			val = int(host_index)
			if not(val > 0 and val <= len(hosts)):
				print("You should enter the index corresponding the option you want. Please, re-run it properly")
			else:
				host = hosts[val-1]
				print("\nHost selected: " + colored(iface, 'green',attrs=['bold']))
				return host
		except ValueError:
			print("You should enter the index corresponding the option you want. Please, re-run it properly")
			return None

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO GET INFORMATION ABOUT BACKGROUND PROCESSES

def __background_processes_info():

	aux = False

	if(not(len(passive_sniffers)==0)):
		aux = True
		print(colored("[*] Passive scanners running at background: ","blue"))
		for passive_sniffer in passive_sniffers:
			print(colored("[*][*] " + passive_sniffer[0],"blue"))

	if(False):
		aux = True
		print("[*] Slowed connections running at background: ")

	if(False):
		aux = True
		print("[*] Fake APs")

		
	if(aux):
		print("[!] DO NOT FORGET TO STOP BACKGROUND PROCESSES WHEN YOU DO NOT NEED IT IN ORDER TO GAIN PERFORMANCE")

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO GET THE NETWORK GIVEN THE IP AND THE NETMASK 

def get_network():
	ip_splitted = interface_ip.split('.')
	mask_splitted = interface_netmask.split('.')
	network = str(int(ip_splitted[0])&int(mask_splitted[0])) 
	network += '.' + str(int(ip_splitted[1])&int(mask_splitted[1]))
	network += '.' + str(int(ip_splitted[2])&int(mask_splitted[2]))
	network += '.' + str(int(ip_splitted[3])&int(mask_splitted[3]))
	return network

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO CHECK IF CERTAIN IP BELONGS TO THE NETWORK SENT BY ARGUMENTS

def belongs_to_network(ip):
	for ips in ipaddress.IPv4Network(get_network() + '/' + str(interface_netmask)):
		if str(ips)==ip:
			return	True

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO GET THE REFRESHED LIST OF ALIVE HOSTS

def get_detected_hosts():
	while (	queue.qsize() != 0 ):
		host = queue.get()
		if ( not(host in detected_hosts) ):
			detected_hosts.append(host)
	return detected_hosts

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO REFRESH AND GET THE ACTIVE PROCESS LIST
	
def get_active_processes():
	# CHECK EACH PROCESS
	for active_process in active_processes:

		# IF IT IS ALIVE, REMOVE IT FROM THE LIST
		active_process[0].join(timeout=0)
		if not( active_process[0].is_alive() ):
			active_processes.remove(active_process)

	# RETURN THE NEW LIST
	return active_processes

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO ADD A NEW PROCESS TO THE ACTIVE PROCESS LIST
def add_active_process(process):
    return 0

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO KILL A PROCESS AND REFRESH THE ACTIVE PROCESS LIST
def stop_active_process(action,param):

	if debug_mode:
		liblog.write_in_file("STOP ACTIVE PROCESS LAUNCHED: " + action + " - " + param)

    # MOVE THROUGH EACH ACTIVE PROCESS
	for active_process in active_processes:

        # CHECK IF IT IS THE PROCESS WE ARE LOOKING FOR
		if (active_process[1] == action):
			if (active_process[2] == param):

                # KILL THE PROCESS
				active_process[0].terminate()
				active_process[0].join()

				# REMOVE IT FROM THE LIST
				active_processes.remove(active_process)

				# RETURN 0: OK
				if debug_mode:
					liblog.write_in_file("PROCESS STOPED")
				return 0
            
    # IF IT HAS NOT BEEN FOUND, RETURN 1
	if debug_mode:
		liblog.write_in_file("ERROR: ACTIVE PROCESS NOT FOUND")
	return 1

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO CREATE AN ACTIVE SCAN IN A NEW PROCESS

def active_scan(iface_name, tries, loops, timespace):

	if debug_mode:
		liblog.write_in_file("ACTIVE SCAN LAUNCHED. PARAMETERS: [IFACE=" + iface_name + ",TRIES=" + str(tries) + ",LOOPS=" + str(loops) + ",TIMESPACE=" + str(timespace) + "]")
    
	# CHECK IF THERE IS ALREADY ANOTHER SCAN INTO THAT NETWORK RUNING
	active_processes_aux = get_active_processes()
	for active_process in active_processes_aux:
		if ( active_process[1] == 'Active Scan' ):
			if ( active_process[2] == iface_name ):
				if debug_mode:
					liblog.write_in_file("ACTIVE SCAN ABORTED. SIMILAR SCAN WAS ALREADY IN PROCESS")
				return 1

	# CREATE THE BACKGROUND PROCESS
	process = multiprocessing.Process(target=active_scan_background, args=(iface_name,tries,loops,timespace,debug_mode,queue))

	# ADD IT TO THE ACTIVE PROCESS LIST
	active_process = [process, 'Active Scan', iface_name]
	active_processes.append(active_process)

	# START IT
	if debug_mode:
		liblog.write_in_file("ACTIVE SCAN STARTED")
	process.start()
	return 0

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO CREATE AN ACTIVE SCAN IN A NEW PROCESS

def active_scan_background(iface_name,tries,loops,timespace,debug_mode,q):

	# CALL THE SCANNER
	new_detected_hosts = was.active_scan(iface_name, tries, loops, timespace, debug_mode)

	# ADD THE RESULTS TO THE LIST
	# TO_DO: ADD SYNCRONIZATION METHODS
	# TO_DO: COMPROBAR SI YA ESTÁN METIDOS
	for new_detected_host in new_detected_hosts:
		q.put(new_detected_host)

	#q.put(['192.168.31.218','a0:af:bd:11:05:53','lenovo','wlan0'])
	#q.put(['192.168.31.148','dc:fb:48:d1:78:47', 'dell','wlan0'])

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO CALL PERFORM THE SLOW-DOWN ATTACK

def slow_down(victim_ip,victim_mac,supplanted_ip,own_mac,interface,timespace):
    
	if debug_mode:
		liblog.write_in_file("SLOW-DOWN LAUNCHED. PARAMETERS: [VICTIM IP=" + victim_ip + ",VICTIM MAC=" + victim_mac + ",TIMESPACE=" + str(timespace) + "]")

    # CHECK IF THERE IS ALREADY ANOTHER SLOW-DOWN ATTACK TO THAT HOST RUNING
	active_processes_aux = get_active_processes()
	for active_process in active_processes_aux:
		if ( active_process[1] == 'Slow Down' ):
			if ( active_process[2] == victim_ip ):
				if debug_mode:
					liblog.write_in_file("SLOW-DOWNN ABORTED. SIMILAR SLOW-DOWN WAS ALREADY IN PROCESS")
				return 1
            
    # CREATE THE BACKGROUND PROCESS
	process = multiprocessing.Process(target=slow_down_background, args=(victim_ip,victim_mac,supplanted_ip,own_mac,interface,timespace))
    
    # ADD IT TO THE ACTIVE PROCESS LIST
	active_process = [process, 'Slow Down', victim_ip]
	active_processes.append(active_process)
    
    # START IT
	if debug_mode:
		liblog.write_in_file("SLOW-DOWN STARTED")
	process.start()
	return 0

# **************************************************************************************
# **************************************************************************************
# AUXILIAR FUNCTION TO EXECUTE AT BACKGROUND THE ATTACK

def slow_down_background(victim_ip,victim_mac,supplanted_ip,own_mac,interface,timespace):
    arps.attack(victim_ip,victim_mac,supplanted_ip,own_mac,interface,timespace)

# **************************************************************************************
# **************************************************************************************
# FUNCTION EXECUTED EACH TIME THE SCANNER SNIFS A NEW PACKET

def new_packet(packet):

	# GETTING THE SOURCE ADDRESSES
	if ARP in packet:
        	ip_src = packet[ARP].psrc
        	hw_src = packet[ARP].hwsrc
	else:
		if ((IP in packet) and (Ether in packet)) :
			ip_src = packet[IP].src
			hw_src = packet[Ether].src
		else:
			return 0

	# CHECKING IF WE HAVE DISCOVERED A NEW VALID HOST:
	# 1, CHECKING IF SOURCE BELONG TO NETWORK
	belongs = belongs_to_network(ip_src)
	if(belongs):
		# 2, CHECKING IF THE SOURCE IS NOT THE GATEWAY
		if(ip_src!=interface_gateway and ip_src!=interface_ip):
			# 3, CHECKING IF THE SOURCE IS ALREADY IN THE LIST
			if not([ip_src,hw_src] in detected_hosts):
				# ADDING THE SOURCE TO THE LIST
				detected_hosts.append([ip_src,hw_src])
				
				# PRINTING DEBUG INFO
				if(debug_mode):
					print("NEW HOST DISCOVERED. HOST DISCOVERED: " + str(detected_hosts))


# **************************************************************************************
# **************************************************************************************
# SETTING THE PASSIVE SNIFFER

#t = AsyncSniffer(iface=ifaces, prn=new_packet, store=False)
#t.start()
#t.stop()

# **************************************************************************************
# **************************************************************************************