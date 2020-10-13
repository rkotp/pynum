# IMPORTS
from flask import *
from lib import interfaces
import lib.main as libmain
import lib.wireless_active_scanner as libwas
import re
from pynum import username
from pynum import password
import random
import string
import hashlib
import datetime

# DEFINE FLASK
app = Flask(__name__)

# DEFINE NEEDED VARIABLES
sessions = []
challenges = []

# **************************************************************************************
# **************************************************************************************

@app.route('/')
def web_main():
    if not( is_logged(request) ):
        return redirect(url_for('web_display_log_in'))
    return render_template('index.html')

# **************************************************************************************
# **************************************************************************************

@app.route('/active-processes')
def web_active_processes():
    if not( is_logged(request,False) ):
        return str(-1)
    active_processes = libmain.get_active_processes()
    active_processes_aux = []
    for active_process in active_processes:
        active_processes_aux.append([active_process[1],active_process[2]])
    return jsonify(len(active_processes_aux),active_processes_aux)

# **************************************************************************************
# **************************************************************************************

@app.route('/kill-process', methods=['POST'])
def web_kill_process():
    if not( is_logged(request) ):
        return str(-1)
    action = request.values.get('action')
    ip = request.values.get('ip')
    aux = libmain.stop_active_process(action,ip)
    return str(aux)

# **************************************************************************************
# **************************************************************************************

@app.route('/hosts-detected')
def web_hosts_detected():
    if not( is_logged(request,False) ):
        return str(-1)
    hd = libmain.get_detected_hosts()
    return jsonify(len(hd),hd)

# **************************************************************************************
# **************************************************************************************

@app.route('/discover')
def web_discover():
    if not( is_logged(request) ):
        return redirect(url_for('web_display_log_in'))
    ifaces = interfaces.ifaces()
    return render_template('detect.html', ifaces=ifaces)

# **************************************************************************************
# **************************************************************************************

@app.route('/start-discover', methods=['POST'])
def start_discover():
    if not( is_logged(request) ):
        return str(-1)
    interface = request.values.get('interface')
    tries = request.values.get('tries')
    loops = request.values.get('loops')
    timespace = request.values.get('time')
    aux = libmain.active_scan(interface, tries, loops, timespace)
    return str(aux)

# **************************************************************************************
# **************************************************************************************

@app.route('/slow-down', methods=['POST'])
def web_slow_down():
    if not( is_logged(request) ):
        return str(-1)
    iface = request.values.get('iface')
    mac = request.values.get('mac')
    ip = request.values.get('ip')
    # VERIFY ALL THIS PARAMETERS ARE WELL FORMED AND INTRODUCED AT THE HOSTS LIST
    mac_pattern = re.compile("([A-F|a-f|0-9]{2}:){5}[A-F|a-f|0-9]")
    ip_pattern = re.compile("((25[0-5]\.|2[0-4][0-9]\.|1[0-9][0-9]\.|[0-9][0-9]\.|[0-9]\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}){1}")
    if ( not( (mac_pattern.match(mac)) or (ip_pattern.match(ip))  ) ):
        return 2
    timespace = request.values.get('time')
    gw = interfaces.iface_netgw(iface)
    o_mac = interfaces.iface_own_mac(iface)           
    print("slow down")
    aux = libmain.slow_down(ip, mac, gw, o_mac, iface, timespace)
    return str(aux)

# **************************************************************************************
# **************************************************************************************

@app.route('/host', methods=['POST'])
def web_host():
    if not( is_logged(request) ):
        return redirect(url_for('web_display_log_in'))
    iface = request.values.get('iface')
    ip = request.values.get('ip')
    mac = request.values.get('mac')
    hostname = request.values.get('hostname')
    return render_template('host.html', iface=iface, ip=ip, mac=mac, hostname=hostname)

# **************************************************************************************
# **************************************************************************************

@app.route('/login')
def web_display_log_in():
    # IF IT IS LOGGED, REDIRECT TO INDEX
    if ( is_logged(request) ):
        return redirect(url_for('web_main'))
    # IF NOT, TO LOGIN
    else:
        # SET A NEW COOKIE
        letters_and_digits = string.ascii_letters + string.digits
        cookie = ''.join((random.choice(letters_and_digits) for i in range(50)))
        resp = make_response(render_template('login.html'))
        resp.set_cookie('session', cookie, httponly=True)
        return resp 

# **************************************************************************************
# **************************************************************************************

@app.route('/challenge')
def challenge():
    # TO_DO: CLEAN UNUSED CHALLENGES

    # GET IP AND COOKIE
    ip_address = request.remote_addr
    if (ip_address is None):
        return False
    ip_pattern = re.compile("((25[0-5]\.|2[0-4][0-9]\.|1[0-9][0-9]\.|[0-9][0-9]\.|[0-9]\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}){1}")
    if ( not( ip_pattern.match(ip_address) ) ):
        return False
    cookie = request.cookies.get('session')
    if ( cookie is None):
        return False
    cookie_pattern = re.compile("[A-Z|a-z|0-9]{50}")
    if ( not( cookie_pattern.match(cookie) ) ):
        return False

    # GENERATE THE CHALLENGE   
    letters_and_digits = string.ascii_letters + string.digits
    proposed_challenge = ''.join((random.choice(letters_and_digits) for i in range(50)))

    # STORE THE CHALLENGE AND THE CORRECT RESPONSE
    response = hashlib.sha256((proposed_challenge + username + password).encode()).hexdigest()
    challenges.append([ip_address, cookie, proposed_challenge, response])

    # SEND THE CHALLENGE TO THE CLIENT
    return proposed_challenge

# **************************************************************************************
# **************************************************************************************

@app.route('/response', methods=['POST'])
def response():
    # DO_DO: CLEAN UNUSED SESSIONS
    # GET IP, COOKIE AND RESPONSE
    ip_address = request.remote_addr
    if (ip_address is None):
        return False
    ip_pattern = re.compile("((25[0-5]\.|2[0-4][0-9]\.|1[0-9][0-9]\.|[0-9][0-9]\.|[0-9]\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}){1}")
    if ( not( ip_pattern.match(ip_address) ) ):
        return False
    cookie = request.cookies.get('session')
    if ( cookie is None):
        return False
    cookie_pattern = re.compile("[A-Z|a-z|0-9]{50}")
    if ( not( cookie_pattern.match(cookie) ) ):
        return False
    response = request.values.get('response')

    # CHECK IF IT IS CORRECT
    for challenge in challenges:
        if (ip_address == challenge[0]) and (cookie == challenge[1]) and (response == challenge[3]):
            sessions.append([ip_address,cookie,datetime.datetime.now()])
            return str(1)

    return str(0)

# **************************************************************************************
# **************************************************************************************

def is_logged(request,aux=True):
    # GET IP, COOKIE AND RESPONSE
    ip_address = request.remote_addr
    if (ip_address is None):
        return False
    ip_pattern = re.compile("((25[0-5]\.|2[0-4][0-9]\.|1[0-9][0-9]\.|[0-9][0-9]\.|[0-9]\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}){1}")
    if ( not( ip_pattern.match(ip_address) ) ):
        return False
    cookie = request.cookies.get('session')
    if ( cookie is None):
        return False
    cookie_pattern = re.compile("[A-Z|a-z|0-9]{50}")
    if ( not( cookie_pattern.match(cookie) ) ):
        return False
    response = request.values.get('response')

    # SEARCH BETWEEN ALL THE SESSIONS
    if (len(sessions)<1):
        return False
    else:
        for session in sessions:
            elapsed_time = (datetime.datetime.now() - session[2]).total_seconds()
            if ( ( session[0] == ip_address ) and ( session[1] == cookie ) and ( elapsed_time < 1800) ):
                # UPDATE THE LAST ACTION TIME (EXCEPT FOR AUTOMATIC ACTIONS)
                if(aux):
                    session[2] = datetime.datetime.now()
                return True
    
    return False

# **************************************************************************************
# **************************************************************************************

@app.route('/logout')
def logout():
    ip_address = request.remote_addr
    if (ip_address is None):
        return False
    ip_pattern = re.compile("((25[0-5]\.|2[0-4][0-9]\.|1[0-9][0-9]\.|[0-9][0-9]\.|[0-9]\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}){1}")
    if ( not( ip_pattern.match(ip_address) ) ):
        return False
    cookie = request.cookies.get('session')
    if ( cookie is None):
        return False
    cookie_pattern = re.compile("[A-Z|a-z|0-9]{50}")
    if ( not( cookie_pattern.match(cookie) ) ):
        return False
    response = request.values.get('response')

    for session in sessions:
            if ( ( session[0] == ip_address ) and ( session[1] == cookie ) ):
                sessions.remove(session)
    
    return redirect(url_for('web_display_log_in'))

# **************************************************************************************
# **************************************************************************************

app.run(host='0.0.0.0', port=9000, debug=True)