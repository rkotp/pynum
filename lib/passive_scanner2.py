# **************************************************************************************************************************
# IMPORTS
import netifaces
from scapy.all import *
import sys
import ipaddress
# **************************************************************************************************************************

# **************************************************************************************************************************
# SET UP DEBUG MODE IF SELECTED
debug_mode = False
if(len(sys.argv) == 3):
	if(sys.argv[2]=='1'):
		debug_mode = True
# **************************************************************************************************************************

# **************************************************************************************************************************
# GETTING THE REST OF ARGUMENTS
interface = sys.argv[1]
this_ip = netifaces.ifaddresses(interface)[2][0]['addr']
gateway = netifaces.gateways()['default'][2][0]
mask = netifaces.ifaddresses(interface)[2][0]['netmask']
mask_cidr = sum(bin(int(x)).count('1') for x in mask.split('.'))
# **************************************************************************************************************************

# **************************************************************************************************************************
# PRINTING DEBUF INFO
if(debug_mode):
	print("** PASSIVE SCAN **")
	print("-> Interface selected: " + interface)
	print("-> Network: ")
	print("-> IP: " + this_ip)
	print("-> Mask: " + mask)
	print("-> Gateways: " + gateway)
# **************************************************************************************************************************

# **************************************************************************************************************************
# AUXILIAR FUNCTION TO GET THE NETWORK GIVEN THE IP AND THE NETMASK
def get_network(ip):
	ip_splitted = ip.split('.')
	mask_splitted = mask.split('.')
	network = str(int(ip_splitted[0])&int(mask_splitted[0])) 
	network += '.' + str(int(ip_splitted[1])&int(mask_splitted[1]))
	network += '.' + str(int(ip_splitted[2])&int(mask_splitted[2]))
	network += '.' + str(int(ip_splitted[3])&int(mask_splitted[3]))
	return network
# **************************************************************************************************************************
# AUXILIAR FUNCTION TO CHECK IF CERTAIN IP BELONGS TO THE NETWORK SENT BY ARGUMENTS
def belongs_to_network(ip):
	for ips in ipaddress.IPv4Network(get_network(this_ip) + '/' + str(mask_cidr)):
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
def detected_ip(packet):

	# PARSE PACKET TO GET IP PARAMETERS
	ip_layer = packet.getlayer(IP)
	if(debug_mode):
		print("[!] New Packet: {src} -> {dst}".format(src=ip_layer.src, dst=ip_layer.dst))
	# CHECKING IF SOURCE BELONG TO NETWORK
	belongs = belongs_to_network(ip_layer.src)
	if(belongs):
		# CHECKING IF THE SOURCE IS NOT THE GATEWAY
		if(ip_layer.src!=gateway and ip_layer.src!=this_ip):
			already_in = is_in_file(ip_layer.src)
			# CHECKING IF THE SOURCE IS ALREADY IN THE LIST
			if(already_in == False):
				# ADDING THE SOURCE TO THE LIST
				if(debug_mode):
					print("NEW HOST DISCOVERED")
				add_to_file(ip_layer.src)
# **************************************************************************************************************************



# **************************************************************************************************************************
# ------------------------------------------------> MAIN <------------------------------------------------------------------
# DEBUG PRINTING
if(debug_mode):
	print("[*] Start sniffing...")

# SNIFERING
sniff(iface=interface, filter="ip", prn=detected_ip)

# DEBUG PRINTING
if(debug_mode):
	print("[*] Stop sniffing")
# **************************************************************************************************************************
