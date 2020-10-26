# **************************************************************************************
# **************************************************************************************
# IMPORTS
import sqlite3
import pathlib
import random
import string
import multiprocessing
from .print_options import *
import random
from scapy.all import *
from termcolor import colored
import subprocess
import os
import lib.interfaces as libifaces
import ipaddress
import lib.wifi_arp_spoofing as arps
import lib.wireless_active_scanner as was
import lib.get_debug as lgd
import lib.log as liblog
import lib.passive_scanner as libps
import lib.database as libdb
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
# AUXILIAR FUNCTION TO GET THE REFRESHED LIST OF ALIVE HOSTS

def get_detected_hosts():
	while (	queue.qsize() != 0 ):
		host = queue.get()
		if ( not(host in detected_hosts) ):
			libdb.insert_host(host[0],host[1],host[2],host[3])
	hosts_db = libdb.get_host()
	for host_db in hosts_db:
		if ( not(host_db in detected_hosts) ):
			detected_hosts.append(host_db)
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
		#libdb.insert_host(new_detected_host[0],new_detected_host[1],new_detected_host[3],new_detected_host[2])

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

def start_passive_scanner(interface):
	libps.start_ps(interface)

# **************************************************************************************
# **************************************************************************************