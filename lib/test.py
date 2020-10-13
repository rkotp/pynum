import socket
import os
from scapy.all import *
import subprocess
import time
import psutil
import signal
import re

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# DEFINIMOS LAS VARIABLES INICIALES NECESARIAS
ip_c1 = '192.168.31.148'
mac_c1 = 'DC:FB:48:D1:78:47'
ip_c2 = '192.168.31.218'
mac_c2 = 'A0:AF:BD:11:05:53'
ip_atk = '192.168.31.226'
mac_atk = 'DC:A6:32:51:E8:FB'

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def medicion_cliente(rol,ip,protocol,logfile,test,mode,param):
    command = "C:\\Users\\"
    if (rol == "1"):
        command = command + "PRGONZALEZ\\"
    elif (rol == "2"):
        command = command + "Ruben\\"
    command = command + "iperf3.exe -c " + ip + " -p 5201 -t 10 -f m"
    if(protocol=="tcp"):
        result = os.popen(command).read()
        line = result.split("\n")[len(result.split("\n"))-4]
    elif (protocol=="udp"):
        command = command + " -u"
        result = os.popen(command).read()
        line = result.split("\n")[len(result.split("\n"))-5]
    aux = re.search("\d+(\.\d+)?\sMbits\/sec",line)        
    velocidad = aux.group()
    if (rol == "1"):
        logfile.write(time.strftime("'%H','%M','%S','%d','%m','%Y',") + "'" + test + "','" + protocol + "','" + mode + "','" + param + "','1','2','" + velocidad.replace(" ","") + "'\n")
    elif (rol == "2"):
        logfile.write(time.strftime("'%H','%M','%S','%d','%m','%Y',") + "'" + test + "','" + protocol + "','" + mode + "','" + param + "','2','1','" + velocidad.replace(" ","") + "'\n")
    print("[*] Velocidad detectada: " + velocidad)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def medicion_servidor(rol,test):
    print("[*] Creando el Servidor iperf3")
    if (rol == "1"):
        output = os.system("C:\\Users\\PRGONZALEZ\\iperf3.exe -s -D")
        print("[*] Servidor creado")
        print("[*] Espera mientas se ejecutan las pruebas por parte de Cliente 2")
        if (test == "2"):
            print("[*] Presione 'enter' en este equipo cuando acaben la prueba 2 en el Cliente 2")
        elif (test == "4"):
            print("[*] Presione 'enter' en este equipo cuando acaben la prueba 4 en el Cliente 2")
    elif (rol == "2"):
        output = os.system("C:\\Users\\Ruben\\iperf3.exe -s -D")
        print("[*] Servidor creado")
        print("[*] Espera mientas se ejecutan las pruebas por parte de Cliente 1")
        if (test == "1"):
            print("[*] Presione 'enter' en este equipo cuando acabe la prueba 1 en el Cliente 1")
        elif (test == "3"):
            print("[*] Presione 'enter' en este equipo cuando acaben la prueba 3 en el Cliente 1")
    input(">>>")
    print("[*] Parando el Servidor iperf3")
    os.system("taskkill /f /im iperf3.exe")
    print("[*] Servidor parado")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def elegir_interfaz():
    print(netifaces.interfaces())

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_first_params():
    year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
    return str(year)+","+str()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def elegir_roles():

    parametros = [10,5,2.5,1.25,0.75,0.375]

    # ELEGIMOS EL ROL DE CADA EQUIPO
    print("\nSe necesitan tres equipos para ejecutar esta prueba. A continuacion se detallan los distintos roles posibles.")
    print("[1] Cliente 1")
    print("[2] Cliente 2")
    print("[3] Atacante")
    print("\nQue rol tiene este equipo?")
    rol = input(">>> ")
    print("\nRol elegido: " + str(rol))

    # CREAMOS EL ARCHIVO FINAL
    archivo=str(rol) + "_" + str(time.time()).replace(".","") + ".csv"
    f = open(archivo, "w")
    f.write("Hora,Minuto,Segundo,Dia,Mes,Anyo,Num. Prueba,TCP o UDP,Con o Sin Ataque,Valor parametros,Cliente,Servidor,velocidad\n")

    # EMPEZAMOS LA PRUEBA
    if (rol=='1'):
        print("\nEmpezando las pruebas:")

        # SE VAN A REALIZAR CINCO VECES TODAS LAS PRUEBAS
        vuelta = 0
        vueltas = 3
        while (vuelta < vueltas):

            vuelta = vuelta + 1

            print()
            print("[*] TEST 1: TCP, Sin//Con ataque, Cliente 1 -> Cliente 2")
            print()
            # PARA MEDIR LA EFICACIA DEL ATAQUE SE VA A REALIZAR UNA MEDICION SIN Y CON ATAQUE PARA CADA PARAMETRO
            for parametro in parametros:
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                print("[*] Presiona 'enter' cuando Cliente 2 lo indique (primera vez)")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c2,"tcp",f,"1","Sin","-")
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                print("[*] Presiona 'enter' primero en el Atacante y acto seguido en este equipo")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c2,"tcp",f,"1","Con",str(parametro))
            print("\n[*] Test 1 terminado")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print()
            print("\n[*] TEST 2: TCP, Sin//Con ataque, Cliente 2 -> Cliente 1")
            print("\n[*] Presiona 'enter' en Cliente 2")
            medicion_servidor(rol,"2")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print()
            print("[*] TEST 3: UDP, Sin//Con ataque, Cliente 1 -> Cliente 2")
            print()
            for parametro in parametros:
                print("[*] Presiona 'enter' cuando Cliente 2 lo indique")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c2,"udp",f,"3","Sin","-")
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                print("[*] Presiona 'enter' cuando Cliente 2 lo indique")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c2,"udp",f,"3","Con",str(parametro))
            print("\n[*] Test 3 terminado")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print()
            print("[*] TEST 4: UDP, Sin//Con ataque, C2 -> C1")
            print("[*] Presiona 'enter' en el Cliente 2")
            print()
            medicion_servidor(rol,"4")

        f.close()
        
    elif (rol=='2'):
        print("\nEmpezando las pruebas:")
        vuelta = 0
        vueltas = 3
        # SE VAN A REALIZAR CINCO VECES TODAS LAS PRUEBAS
        while (vuelta < vueltas):
            
            vuelta = vuelta + 1
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 1: TCP, Sin//Con ataque, Cliente 1 -> Cliente 2")
            print("\n[*] Presiona 'enter' en el Cliente 1")
            print()
            medicion_servidor(rol,"1")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 2: TCP, Sin//Con ataque, C2 -> C1\n")
            for parametro in parametros:
                print("[*] Presiona 'enter' cuando Cliente 1 lo indique")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c1,"tcp",f,"2","Sin",str(parametro))
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                print("[*] Presiona 'enter' primero en el Atacante y acto seguido en este equipo")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c1,"tcp",f,"2","Con",str(parametro))
            print("\n[*] Test 2 terminado")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 3: UDP, Sin//Con ataque, Cliente 1 -> Cliente 2")
            print("\n[*] Presiona 'enter' en el Cliente 1")
            print()
            medicion_servidor(rol,"1")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\nTEST 4: UDP, Sin//Con ataque, C2 -> C1")
            for parametro in parametros:
                print("[*] Presiona 'enter' cuando Cliente 1 lo indique")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c1,"udp",f,"4","Sin",str(parametro))
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                print("[*] Presiona 'enter' cuando Cliente 1 lo indique")
                input(">>>")
                print("[*] Analizando")
                medicion_cliente(rol,ip_c1,"udp",f,"4","Con",str(parametro))
            print("\n[*] Test 4 terminado")
            print("\n[*] Pulsar 'enter' en Cliente 1")

        print("\n[*] PRUEBAS TERMINADAS")
        f.close()

    elif (rol=='3'):
        print("\nEmpezando las pruebas:")

        vuelta=0
        vueltas=3
        while (vuelta < vueltas):
            vuelta = vuelta + 1
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 1: TCP, Sin//Con ataque, C1 -> C2")
            for parametro in parametros:
                print("[*] Presiona 'enter' en este equipo cuando lo indique Cliente 1 para posteriormente presionar 'enter' en Cliente 1")
                input(">>>")
                print("[*] Atacando, parametro: " + str(parametro))
                result = os.popen("timeout 10 python3 -c 'from wifi_arp_spoofing import attack; attack([\"" + ip_c1 + "\",\"" + mac_c1 + "\"],\"" + ip_c2 + "\",\"" + mac_atk + "\",\"wlan0\"," + str(parametro) + ")'").read()
                print("[*] Ataque terminado")
            print("[*] Presiona 'enter' en el Cliente 2 si el Cliente 1 muestra este mismo mensaje")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 2: TCP, Sin//Con ataque, C2 -> C1")
            for parametro in parametros:
                print("[*] Presiona 'enter' en este equipo cuando lo indique Cliente 2 para posteriormente presionar 'enter' en Cliente 2")
                input(">>>")
                print("[*] Atacando, parametro: " + str(parametro))
                result = os.popen("timeout 10 python3 -c 'from wifi_arp_spoofing import attack; attack([\"" + ip_c2 + "\",\"" + mac_c2 + "\"],\"" + ip_c1 + "\",\"" + mac_atk + "\",\"wlan0\"," + str(parametro) + ")'").read()
                print("[*] Ataque terminado")
            print("[*] Presiona 'enter' en el Cliente 2 si el Cliente 1 muestra este mismo mensaje")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 3: UDP, Con ataque, C1 -> C2")
            for parametro in parametros:
                print("[*] Presiona 'enter' en este equipo cuando lo indique Cliente 1 para posteriormente presionar 'enter' en Cliente 1")
                input(">>>")
                print("[*] Atacando, parametro: " + str(parametro))
                result = os.popen("timeout 10 python3 -c 'from wifi_arp_spoofing import attack; attack([\"" + ip_c1 + "\",\"" + mac_c1 + "\"],\"" + ip_c2 + "\",\"" + mac_atk + "\",\"wlan0\"," + str(parametro) + ")'").read()
                print("[*] Ataque terminado")
            print("[*] Presiona 'enter' en el Cliente 2 si el Cliente 1 muestra este mismo mensaje")
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            print("\n[*] TEST 4: UDP, Con ataque, C2 -> C1")
            for parametro in parametros:
                print("[*] Presiona 'enter' en este equipo cuando lo indique Cliente 2 para posteriormente presionar 'enter' en Cliente 2")
                input(">>>")
                print("[*] Atacando, parametro: " + str(parametro))
                result = os.popen("timeout 10 python3 -c 'from wifi_arp_spoofing import attack; attack([\"" + ip_c2 + "\",\"" + mac_c2 + "\"],\"" + ip_c1 + "\",\"" + mac_atk + "\",\"wlan0\"," + str(parametro) + ")'").read()
                print("[*] Ataque terminado")
            print("[*] Presiona 'enter' en el Cliente 1 si el Cliente 2 muestra este mismo mensaje")

        print("\n[*] PRUEBAS TERMINADAS")



def main():
    elegir_roles()

main()
