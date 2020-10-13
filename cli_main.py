import lib.main as libmain
import lib.interfaces as libifaces
import lib.print_options as libpo
from termcolor import colored

# PRINTING THE BANNER
libmain.initial_banner()

# CORE
while 1:

    # GETTING ALL THE INTERFACES, ACTIVE PROCESSES AND DETECTED HOSTS
    ifaces = libifaces.ifaces()
    active_processes = libmain.get_active_processes()
    detected_hosts = libmain.get_detected_hosts()

    # PRINTING INFO ABOUT BACKGROUND PROCESSES (IMPORTANT TO GET BETTER PERFORMANCE)
    print(colored("\n[*] WARNING: Background processes could slow down the service performance. Please, be sure to keep runing just those strictly necessary. You can check the background process with the \"show-processes\" command.","red"))

    # ASKING FOR THE OPERATION MODE
    print("\nListening to operation mode (type \"options\" to display all posibilities):\n>>> ", end="")
    op_mode = input()
    op_mode = op_mode.lower()
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    if(op_mode==""):
        pass
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="options"):
        libpo.commands()
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
    
    elif(op_mode=="show-ifaces"):
        ifaces = libifaces.ifaces()
        libifaces.show_ifaces(ifaces)
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="show-hosts"):
        detected_hosts = libmain.get_detected_hosts()
        if(not(len(detected_hosts)==0)):
            for detected_host in detected_hosts:
                print(colored("[*] " + detected_host[0] + ", " + detected_host[2],"green"))
        else:
            print("There are no hosts detected yet. Try runing an active or a passive scan. Both options differs on network/device performance and the noise they make. Ensure to understand both methods before runing them.")
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif(op_mode=="show-processes"):
        active_processes = libmain.get_active_processes()
        if(not(len(active_processes)==0)):
            print("")
            i = 0
            for active_process in active_processes:
               print("[" + str(i) + "] - " + active_process[1] + " ( " + active_process[2] + " )")
        else:
            print("There are not current processes runing in background")
            
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="kill-process"):
        active_processes = libmain.get_active_processes()
        if(not(len(active_processes)==0)):
            print("Select one of the following processes (type its id):\n")
            i = 1
            for active_process in active_processes:
               print("[" + str(i) + "] - " + active_process[1] + " ( " + active_process[2] + " )")
               i = i + 1
            process_id = input()
            if((int(process_id) > 1) and (int(process_id) <= i)):
                j = 1
                for active_process in active_processes:
                    if(j == int(process_id)):
                        stop_active_process(active_process[1],active_process[2])
                    j = j + 1
            else:
                print(colored("Selected process not valid","red"))
        else:
            print("There are not current processes runing in background")

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="active-scan"):
        ifaces = libifaces.ifaces()
        active_processes = libmain.get_active_processes()
        # IF THERE ARE NOT INTERFACES UP, THE TASK COULD NOT BEC PERFORMED
        if(len(ifaces)<1):
            print(colored("There should be at least one interface up.","red"))
            exit()

        # ASK FOR THE PARAMETERS
        iface = libmain.select_interface(ifaces)
        print("Select the number of tries [1]:")
        tries = input(">> ")
        if(tries == ""):
            tries = 1
        elif (int(tries) < 1):
            print(colored("Input a valid number of tires.","red"))
        print("Select the number of loops [1]:")
        loops = input(">> ")
        if(loops==""):
            loops = 1
        elif(int(loops) < 1):
            print(colored("Input a valid number of loops.","red"))
        print("Select the timespace [1]:")
        timespace = input(">> ")
        if(timespace==""):
            timespace = 1
        elif(int(timespace) < 1):
            print(colored("Input a valid timespace.","red"))
            
        # PERFORM THE ATTACK
        aux = libmain.active_scan(iface[0], int(tries), int(loops), int(timespace))
        if(aux==1):
            print(colored("\nThere is already running another process with the same purpose","red"))
        elif(aux==0):
            print("\nThe task have been launched. It may take several minutes. You can see the results with the 'list-hosts' command")
            active_processes = libmain.get_active_processes()
        else:
            print(colored("\nAn error have been found while searching for new hosts. Restart the service and try it again. If it persists, contact the develper at https://github.com/rkotp","red"))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="slow-down"):

        ifaces = libifaces.ifaces()
        active_processes = libmain.get_active_processes()
        detected_hosts = libmain.get_detected_hosts()
        
        # CHECKING IF THERE ARE DETECTED HOSTS
        if(len(detected_hosts)>0):
            print("Select one of the following hosts (type its id):\n")

            # PRINT EACH HOST FOR SELECTING IT
            i = 1
            for detected_host in detected_hosts:
                print(colored("[" + str(i) + "] " + detected_host[0] + ", " + detected_host[2],"green"))
                i = i + 1
            host_id = input("\n>>")

            # CHECKING IF THE HOST IS PROPERLY SELECTED
            if((int(host_id) >= 1) and (int(host_id) <= i)):
                j = 1

                # GO THROUGHT ALL THE HOSTS TO ACCESS THE SELECTED HOST AND ITS DATA
                for detected_host in detected_hosts:
                    if(j == int(host_id)):

                        # SELECT THE TIMESPACE AND CHECK IF IT IS PROPERLY SELECTED
                        print("\nSelect the timespace [1]: ")
                        timespace = input(">> ")
                        if(timespace==""):
                            timespace = 1

                            # PERFORM THE ATTACK
                            libmain.slow_down(detected_host[0],detected_host[1],libifaces.iface_netgw(detected_host[3]),libifaces.iface_own_mac(detected_host[3]),int(timespace))
                        
                        elif(int(timespace) > 0):

                            # PERFORM THE ATTACK
                            libmain.slow_down(detected_host[0],detected_host[1],libifaces.iface_netgw(detected_host[3]),libifaces.iface_own_mac(detected_host[3]),int(timespace))

                        else:
                            print(colored("Input a valid timespace.","red"))
                    
                    else:
                        j = j + 1
            
            else:
                print(colored("Please, select a valid host id!","red"))
        
        else:
            print("This task could not be performed. There are no hosts detected yet. Try runing an active or a passive scan. Both options differs on network/device performance and the noise they make. Ensure to understand both methods before runing them.")
            
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    elif(op_mode=="exit" or op_mode=="quit"):
        print("\nThank you for using PYNUM.")
        print("Do not forget to give us feedback about this tool at " + colored("https://github.com/rkotp/pynum","green"))
        print("Hope to see you soon.")
        print("Bye.\n")
        exit()
    
    # ****************************************************************************************************************************************
    # ****************************************************************************************************************************************
    # TO-DO: FUTURE FEATURES TO DEPLOY
    
    # TO-DO: EDIT THE CONFIGURATION FILE THROUGH THIS FUNCTION
    elif(op_mode=="setup"):
        pass

    # TO-DO: ARP-SPOOFING ATTACK WITH DYNAMIC TIMESPACE VALUE
    elif(op_mode=="smart-pause"):
        pass

    # TO-DO: HIDE THE WIFI NETWORK BY FLOODING THE DEVICE NETWORK MANAGER WITH BEACONS OF TONS OF RANDOM NETWORK
    elif(op_mode=="hide"):
        pass
    
    # TO-DO: SEND A DISSASOCIATION SIGNAL TO THE ACCESS POINT SPOOFING A DEVICE IN ORDER TO DISCONNECT IT FROM THE NETWORK
    elif(op_mode=="disconnect-device"):
        pass
        
    elif(op_mode=="passive-scan start"):
        # TO_DO: PRINT DEBUG
        selected_iface = select_interface(ifaces)
        if(selected_iface==None):
            print(colored("[!] No interface selected. Run it again selecting a proper identificator","red"))

        # TO_DO: CHECK PASSIVE SCANNERS AT INTERFACE 
        if(passive_sniffer==None):
            passive_sniffer = AsyncSniffer(iface=selected_iface, prn=new_packet, store=False)
            passive_sniffer.start()
            passive_sniffer.append(selected_iface)
            if(debug_mode):
                print(colored("[*] Passive scanner now running at " + selected_iface + ".","blue"))
                print(colored("[!] ATENTION: Please remember that this scanner is constantly executing at background and that consume resources. As much scanners you star, lower performance you will have. Keep this in mind and stop the scanners when you stop using them."))
            else:
                print(colored("Unable to start a passive scanner: There is already one passive scanner at interface " + selected_iface + ". Use the command 'passive-scan stop' to stop that scanner and re-run this command to establish a new one.","red"))
			
    elif(op_mode=="passive-scan stop"):
        # TO_DO: SELECT PASSIVE SCANNER RUNNING
        # TO_DO: PRINT DEBUG
        scanner_selected.stop()
        # TO-DO: MATCHEAR EN EL IF ANTERIOR CON UNA EXPRESIÓN REGULAR Y FOLLARME ESTE IF
        print("TO-DO: WHATEVER")
        
    else:
        print(colored("Operation mode not valid. Please read the documentation or type \"help\" to list avaible commands","red"))