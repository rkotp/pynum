# **************************************************************************************************************************
# IMPORTS
import netifaces
from scapy.all import * as sc
import sys
import ipaddress
# **************************************************************************************************************************

# **************************************************************************************************************************
# GETTING THE REST OF ARGUMENTS
discovered_hosts = []
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION TO GET THE NETWORK GIVEN THE IP AND THE NETMASK
def get_network(ip,mask):
	ip_splitted = ip.split('.')
	mask_splitted = mask.split('.')
	network = str(int(ip_splitted[0])&int(mask_splitted[0])) 
	network += '.' + str(int(ip_splitted[1])&int(mask_splitted[1]))
	network += '.' + str(int(ip_splitted[2])&int(mask_splitted[2]))
	network += '.' + str(int(ip_splitted[3])&int(mask_splitted[3]))
	return network
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION TO CHECK IF CERTAIN IP BELONGS TO THE NETWORK SENT BY ARGUMENTS
def belongs_to_network(ip,network_ip,network_mask):
	for ips in ipaddress.IPv4Network(get_network(network_ip) + '/' + str(network_mask)):
		if str(ips)==ip:
			return	True
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION TO SEARCH IF AN IP IS ALREADY DISCOVERED
def is_in_file(ip):
	filename = 'passive_ips_detected.txt'
	with open(filename) as f:
		content = f.read().splitlines()
	if (ip in content):
		return True
	else:
		return False
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION TO ADD AN IP DISCOVERED TO THE ACTIVE_IPS FILE
def add_to_file(ip):
	hs = open("passive_ips_detected.txt","a")
	hs.write(ip + "\n")
	hs.close() 
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION EXECUTED WHEN A NEW PACKET IS SNIFFERED
def detected_ip(packet,network_ip,network_mask):

	print(packet)
	# PARSE PACKET TO GET IP PARAMETERS
	ip_layer = packet.getlayer(IP)
	#link_layer = packet.getlayer(Ethernet)

	# DEBUG PRINTING
	if(debug_mode):
		print("[!] New Packet: {src} -> {dst}".format(src=ip_layer.src, dst=ip_layer.dst))
	
	# CHECKING IF WE HAVE DISCOVERED A NEW HOST:
	# 1, CHECKING IF SOURCE BELONG TO NETWORK
	belongs = belongs_to_network(ip_layer.src,network_ip,network_mask)
	if(belongs):
		# 2, CHECKING IF THE SOURCE IS NOT THE GATEWAY
		if(ip_layer.src!=gateway and ip_layer.src!=this_ip):
			#already_in = is_in_file(ip_layer.src)
			# 3, CHECKING IF THE SOURCE IS ALREADY IN THE LIST
			#if(already_in == False):
			if not(ip_layer.src in discovered_hosts):
				# ADDING THE SOURCE TO THE LIST
				if(debug_mode):
					print("NEW HOST DISCOVERED")
				add_to_file(ip_layer.src)
				discovered_hosts.append(["",""])
# **************************************************************************************************************************

# **************************************************************************************************************************
# MAIN FUNCTION
def scan(interface,debug):

	# DEBUG PRINTING
	if(debug_mode):
		print("[*] Start sniffing...")

	# SNIFERING
	sc.sniff(iface=interface[0], filter="ip", prn=detected_ip(interface))

	# DEBUG PRINTING
	if(debug_mode):
		print("[*] Stop sniffing")

# **************************************************************************************************************************