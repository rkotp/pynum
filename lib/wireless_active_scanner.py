# IMPORTS
import socket
import time
import netifaces
from scapy.all import *
import sys
import ipaddress
from termcolor import colored
import lib.interfaces as libifaces
import lib.log as liblog

# **************************************************************************************************************************
# **************************************************************************************************************************
# MAIN FUNCTION: IT GETS NETWORK INFO BASED ON THE INTERFACE AND CALL THE FUNCTION THAT EXECUTES THE SCANNER

# TO_DO: METER LOS PRINTS DENTRO DEL IF DEL DEBUG

def active_scan(iface, tries, loops, timespace, debug_mode):

	detected_hosts = []

	# GET ALL THE POSSIBLE NETWORK HOST ADDRESSES
	iface_address = libifaces.iface_addr(iface)
	network_address = libifaces.iface_netaddr(iface)
	network_gateway = libifaces.iface_netgw(iface)
	netmask = libifaces.iface_netmask(iface)
	netmask_cidr = 0
	for x in netmask.split('.'):
		netmask_cidr = netmask_cidr + bin(int(x)).count('1')
	ip_addresses = ipaddress.IPv4Network(network_address + '/' + str(netmask_cidr))

	# GO THROUGH EACH LOOP
	for loop in range(int(loops)):

		# GO THROUGH EACH IP
		for ips in ip_addresses:

			# REPEAT EACH IP
			for rep in range(int(tries)):

				# IF IT IS THE GATEWAY OR OURSELVES CONTINUE TO NEXT ITERATION
				if not( (str(ips)==iface_address) or (str(ips)==network_gateway) or (str(ips).endswith('.0')) ):
				
					# ARP REQUEST
					time.sleep(int(timespace))
					arp_frame = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=str(ips))
					ans,unans = srp(arp_frame,iface=iface,timeout=1,verbose=0)
					if debug_mode:
						liblog.write_in_file("ARP REQUEST SENT TO " + str(ips))
					print("Scanning ip: " + str(ips))

					# IF ANSWER RECEIVED -> HOST ALIVE
					for snt,recv in ans:
						if recv:
							#print(socket.gethostbyaddr(str(recv[ARP].psrc))[0])
							hostname = 'Unknown hostname'
							detected_hosts.append([str(recv[ARP].psrc),str(recv[Ether].src),hostname,iface])
							if debug_mode:
								liblog.write_in_file("HOST DETECTED: " + str(ips))
							print(colored("[*]","blue") + " Host Alive: " + recv[ARP].psrc + " - " + recv[Ether].src)

	# RETURN THE HOSTS ALIVE
	return detected_hosts

# **************************************************************************************************************************
# **************************************************************************************************************************