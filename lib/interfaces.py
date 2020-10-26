# IMPORTS
import netifaces
from termcolor import colored
# **************************************************************************************
# **************************************************************************************
def get_ifaces_names():
	ifaces = netifaces.interfaces()
	i = 0
	while i < len(ifaces):
		if(ifaces[i]=='lo'):
			ifaces.pop(i)
		i+=1
	return ifaces
# **************************************************************************************
# **************************************************************************************
def iface_own_mac(iface):
	return netifaces.ifaddresses(iface)[17][0]['addr']
# **************************************************************************************
# **************************************************************************************
def iface_addr(iface):
	return netifaces.ifaddresses(iface)[2][0]['addr']
# **************************************************************************************
# **************************************************************************************
def iface_netmask(iface):
	return netifaces.ifaddresses(iface)[2][0]['netmask']
# **************************************************************************************
# **************************************************************************************
def iface_netgw(iface):
	return netifaces.gateways()['default'][2][0]
# **************************************************************************************
# **************************************************************************************
def iface_netaddr(iface):
	ip_splitted = iface_addr(iface).split('.')
	mask_splitted = iface_netmask(iface).split('.')
	network = str(int(ip_splitted[0])&int(mask_splitted[0])) 
	network += '.' + str(int(ip_splitted[1])&int(mask_splitted[1]))
	network += '.' + str(int(ip_splitted[2])&int(mask_splitted[2]))
	network += '.' + str(int(ip_splitted[3])&int(mask_splitted[3]))
	return network
# **************************************************************************************
# **************************************************************************************

def ifaces():
	
	# ARRAY WITH INTERFACES UP AT THE HOST
	ifaces = []
	aux = []

	# EACH IFACE IS AN ARRAY COMPOSED BY NAME, IP, NETWORK, NETMASK AND GATEWAY
	aux = netifaces.interfaces()

	i = 0
	while i < len(aux):

		iface = aux[i]
		if(aux[i]=='lo' or len(netifaces.ifaddresses(iface))<3):
			aux.pop(i)

		else:
			ifaces.append([iface,iface_netaddr(iface),iface_netmask(iface),iface_netgw(iface),iface_addr(iface)])
			i+=1

	
	return ifaces

def show_ifaces(ifaces):
	for iface in ifaces:
		print("\n" + colored("[*]","blue") + " Interface: " + iface[0] + "\n[*] Network address: " + iface[1] + "\n[*] Netwok mask: " + iface[2] + "\n[*] Gateway: " + iface[3] + "\n[*] IP Address: " + iface[4] + "\n[*] Channel:\n-------------------------------------")
