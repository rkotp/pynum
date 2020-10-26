# **************************************************************************************************************************
# **************************************************************************************************************************
# IMPORTS
import xml.etree.ElementTree as ET
import pathlib
from netaddr import IPNetwork, IPAddress
import lib.interfaces as libifaces
import scapy.all as sc
import sqlite3
import lib.get_debug as lgd
import lib.log as liblog
import lib.database as libdb
from termcolor import colored
# **************************************************************************************************************************
# **************************************************************************************************************************

# **************************************************************************************************************************
# **************************************************************************************************************************
#LIST WITH DETECTED IPS
detected_hosts = []
debug_mode = lgd.get_dbg()
# **************************************************************************************************************************
# **************************************************************************************************************************

# **************************************************************************************************************************
# **************************************************************************************************************************
# RETURNS TRUE IF PASSIVE SCANNER IS SET BY DEFAULT, FALSE IN ANOTHER CASE
def get_ps():

	# READ CONFIGURATION FILE
	xml_file = str(pathlib.Path(__file__).parent.parent.absolute()) + "/config.xml"
	xmlTree = ET.parse(xml_file)
	rootElement = xmlTree.getroot()

  # GET THE DEBUG MODE
	ps_aux = rootElement.findall("./passive_scanner")

  # CHECK IF IT IS PROPERLY SET
	if (not(len(ps_aux)==1)):
		return [False,0]
	ps = ps_aux[0].text
	if (not( ps.lower() == 'yes' or ps.lower() =='no' )):
		return [False,1]

  # IF IT IS SET TO 'NO' RETURN FALSE
	if ( ps.lower() == 'no' ):
		return [False,2]

	# IF IT IS SET TO TRUE, CHECK THE IFACE
	elif ( ps.lower() == 'yes' ):
		psiface_aux = rootElement.findall("./passive_scanner_interface")
		if (not(len(psiface_aux)==1)):
			return [False,3]
		ps_iface = psiface_aux[0].text
		if ps_iface in libifaces.get_ifaces_names():
			return [True,ps_iface]
		else:
			return [False,4]

# **************************************************************************************************************************
# **************************************************************************************************************************

# **************************************************************************************************************************
# **************************************************************************************************************************
# FUNCTION TO STAR THE PASSIVE SNIFFER
def start_ps(interface):

	# FIRST, CHECK IF IT IS ALREADY LAUNCHED
	iface_aux = libdb.get_iface_ps()
	if( not( len(iface_aux)==0 )):
		return 0
		 
	print(colored("[*] STARTING PASSIVE SCANNER","blue"))

	# SNIFERING
	ps = sc.AsyncSniffer(iface=interface, prn=ps_packet_handler, store=False)
	ps.start()

	libdb.insert_process('Passive Scanner',interface)
	print(colored("[*] PASSIVE SCANNER STARTED","blue"))
	return ps

# **************************************************************************************************************************
# **************************************************************************************************************************

# **************************************************************************************************************************
# **************************************************************************************************************************
# AUXILIAR FUNCTION TO STOP THE PASSIVE SCANNER
def stop_ps(ps):
	ps.stop()
# **************************************************************************************************************************
# **************************************************************************************************************************



# **************************************************************************************************************************
# **************************************************************************************************************************
# THIS FUNCTION IS GOING TO BE CALLED EACH TIME A PACKET IS CAPTURED BY THE SNIFFER
def ps_packet_handler(packet):
	
	# GET THE SOURCE ADDRESSES (IP AND MAC)
	if sc.ARP in packet:
		ip_src = packet[sc.ARP].psrc
		hw_src = packet[sc.ARP].hwsrc
	else:
		if ((sc.IP in packet) and (sc.Ether in packet)) :
			ip_src = packet[sc.IP].src
			hw_src = packet[sc.Ether].src
		else:
			return 0

	# GETTING NOT VALID IPS
	iface = libdb.get_iface_ps()[0][0]
	not_valid_directions = []
	not_valid_directions.append(libifaces.iface_addr(iface))
	not_valid_directions.append(libifaces.iface_netgw(iface))
	not_valid_directions.append(libifaces.iface_netaddr(iface))

	# CHECK IF THE SOURCE IP BELONGS TO THE NETWORK
	if IPAddress(ip_src) in IPNetwork(libifaces.iface_addr(iface) + "/" + str(IPAddress(libifaces.iface_netmask(iface)).netmask_bits())):
		# CHECK IF THE SOURCE IP IS NOT ONE OF THOSE INVALID IPS
		if( not(ip_src in not_valid_directions) ):
			# CHECK IF IT IS ALREADY DETECTED
			if not([ip_src,hw_src] in detected_hosts):
				# ADDING THE SOURCE TO THE LIST
				print(colored("[*] HOST PASSIVELY DETECTED: " + str(ip_src) + ", " + str(hw_src),"green"))
				libdb.insert_host(str(ip_src),str(hw_src),iface,'Unknown hostname')
				
				detected_hosts.append([ip_src,hw_src])

# **************************************************************************************************************************
# **************************************************************************************************************************

# **************************************************************************************************************************
# **************************************************************************************************************************
# THE FUNCTION WILL RETURN THE DETECTED HOSTS AND CLEAR THE INTERNAL LIST
def ps_get_detected_hosts():
	returned_list = detected_hosts
	detected_hosts = []
	return returned_list
# **************************************************************************************************************************
# **************************************************************************************************************************