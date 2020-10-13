# **************************************************************************************
# **************************************************************************************
# IMPORTS

from termcolor import colored
import random
import pathlib

# **************************************************************************************
# **************************************************************************************
# MAIN FUNCTION - DISPLAY THE LIST OF OPERATION MODES AND ITS DESCRIPTION

def initial_banner():
    # RANDOM NUMBER BETWEEN 1 AND 12
    banner_file = str(pathlib.Path(__file__).parent.absolute()) + "/banner/banner.txt"
    # READ THE FILE
    file = open(banner_file,'r')
    # PRINT THE FILE
    print("\n")
    print(file.read())
    print("PYthon based Network Users Manager")
    print("Author: Pedro Rubén González Sánchez")
    print("Supervised by: Pablo Serrano")
    print("License: GNU General Public License v3.0")
    print("Url: " + colored("https://github.com/rkotp/pynum","green"))
    print("\n***************************************************************")
    print("***************************************************************")
    if not os.geteuid() == 0:
        print(colored("\nYou are not running the service as root. This may lead into troubles in certain capabilities. It would be better if you re-run it with 'sudo'","red"))

# **************************************************************************************
# **************************************************************************************
# MAIN FUNCTION - DISPLAY THE LIST OF OPERATION MODES AND ITS DESCRIPTION

def final_banner():
    return "hola"

# **************************************************************************************
# **************************************************************************************
# MAIN FUNCTION - DISPLAY THE LIST OF OPERATION MODES AND ITS DESCRIPTION

def background_processes_info(passive_sniffers,current_spoofings):

	if( not(len(passive_sniffers)==0) and not(len(current_spoofings)==0) ):
		print(colored("\n[!] DO NOT FORGET TO STOP BACKGROUND PROCESSES WHEN YOU DO NOT NEED IT IN ORDER TO GAIN PERFORMANCE", "red", attrs=['bold']))

	if(not(len(passive_sniffers)==0)):
		print(colored("[*] Passive scanners running at background: ","blue"))
		for passive_sniffer in passive_sniffers:
			print(colored("[*][*] " + passive_sniffer[0],"blue"))

	if(False):
		print("[*] Slowed connections running at background: ")

	if(False):
		print("[*] Fake APs")

		
	
# **************************************************************************************
# **************************************************************************************
# MAIN FUNCTION - DISPLAY THE LIST OF OPERATION MODES AND ITS DESCRIPTION

def commands():
    print("\nAVAILABLE COMMANDS:\n")
    print(colored("[-]","blue") + " 'options': Displays the list of available commands.")
    print(colored("[-]","blue") + " 'show-ifaces': List the available interfaces.")
    print(colored("[-]","blue") + " 'show-hosts': Enumerate all the detected hosts.")
    print(colored("[-]","blue") + " 'show-processes': Show the active processes. Remember to kill thoose unnecesaries.")
    print(colored("[-]","blue") + " 'kill-process': Kill active process.")
    print(colored("[-]","blue") + " 'active-scan': Detect actively all the hosts at the network. This could be potentially dangerous. Be sure to understand the difference between active and passive scan.")
    print(colored("[-]","blue") + " 'slow-down': Slow-down the connection speed of a given host. You can slow-down the speed until it reaches 0 Mbps.")
    print(colored("[-]","blue") + " 'exit' | 'quit': Exits the service")
    print("\nYou can review the full documentation at " + colored("https://www.github.com/rkotp/pynum","green") + ".")
    print("Leave us there your comments, errors detected or features you encourage us to develop.")

# **************************************************************************************
# **************************************************************************************