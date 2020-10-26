# **************************************************************************************
# **************************************************************************************

import sqlite3
import pathlib
from termcolor import colored

# **************************************************************************************
# **************************************************************************************

def initialize_database():
    print(colored("[*] INITIALIZING DATABASE","magenta"))
    conn = sqlite3.connect(str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS detected_host (ip, mac, interface, hostname)")
    c.execute("DELETE FROM detected_host")
    c.execute("CREATE TABLE IF NOT EXISTS active_process (type,data)")
    c.execute("DELETE FROM active_process")
    conn.commit()
    conn.close()

# **************************************************************************************
# **************************************************************************************

def insert_host(ip,mac,iface,hostname):
    print(colored("[*] INSERTING HOST INTO DATABASE","magenta"))
    conn = sqlite3.connect(str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.db")
    c = conn.cursor()
    query  = "SELECT * FROM detected_host WHERE ip='" + str(ip) + "' AND mac='" + str(mac) + "' AND interface='" + iface + "' AND hostname='Unknown host';"
    c.execute(query)
    if( len(c.fetchall()) == 0 ):
        c.execute("INSERT INTO detected_host VALUES ('" + str(ip) + "','" + str(mac) + "','" + iface + "','" + hostname + "');")
        print(colored("[*] HOST INSERTED INTO DATABASE","magenta"))
    else:
        print(colored("[*] HOST ALREADY INSERTED INTO DATABASE","magenta"))
    conn.commit()
    conn.close()

# **************************************************************************************
# **************************************************************************************

def get_host():
    conn = sqlite3.connect(str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.db")
    c = conn.cursor()
    c.execute("SELECT * FROM detected_host")
    hosts = c.fetchall()
    conn.commit()
    conn.close()
    return hosts

# **************************************************************************************
# **************************************************************************************

def insert_process(type,data):
    print(colored("[*] INSERTING PROCESS INTO DATABASE","magenta"))
    conn = sqlite3.connect(str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.db")
    c = conn.cursor()
    query  = "SELECT * FROM active_process WHERE type='" + str(type) + "' AND data='" + str(data) + "';"
    c.execute(query)
    value = c.fetchall()
    if( len(value) == 0 ):
        c.execute("INSERT INTO active_process (type, data) VALUES ('" + str(type) + "','" + str(data) + "');")
        print(colored("[*] INSERTED PROCESS INTO DATABASE","magenta"))
    conn.commit()
    conn.close()

# **************************************************************************************
# **************************************************************************************

def get_iface_ps():
    conn = sqlite3.connect(str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.db")
    c = conn.cursor()
    c.execute("SELECT data FROM active_process WHERE type = 'Passive Scanner'")
    iface = c.fetchall()
    conn.commit()
    conn.close()
    return iface
