# IMPORTS
import xml.etree.ElementTree as ET
import pathlib
import lib.get_debug as lgd
import lib.log as liblog

liblog.write_in_file("PYNUM STARTED")

# READ CONFIGURATION FILE
xml_file = str(pathlib.Path(__file__).parent.absolute()) + "/config.xml"
xmlTree = ET.parse(xml_file)
rootElement = xmlTree.getroot()

# GET THE USER INTERFACE MODE
ui_aux = rootElement.findall("./ui_mode")
if (not(len(ui_aux)==1)):
    liblog.write_in_file("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    print("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    exit()
ui = ui_aux[0].text
if (not( ui=='gui' or ui=='cli' )):
    liblog.write_in_file("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    print("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    exit()

# GETTING THE USERNAME AND THE PASSWORD
username_aux = rootElement.findall("./usr")
if (not(len(username_aux)==1)):
    liblog.write_in_file("ERROR: USERNAME NOT PROPERLY SET IN THE CONFIG FILE")
    print("ERROR: USERNAME NOT PROPERLY SET IN THE CONFIG FILE")
    exit()
username = username_aux[0].text
password_aux = rootElement.findall("./pwd")
if (not(len(password_aux)==1)):
    liblog.write_in_file("ERROR: PASSWORD NOT PROPERLY SET IN THE CONFIG FILE")
    print("ERROR: PASSWORD NOT PROPERLY SET IN THE CONFIG FILE")
    exit()
password = password_aux[0].text

# CHECK IF DEBUG MODE IS SET
if (lgd.get_dbg()[0] == -1):
    liblog.write_in_file("ERROR: DEBUG MODE NOT PROPERLY SET IN THE CONFIG FILE")
    print("DERROR: EBUG MODE NOT PROPERLY SET IN THE CONFIG FILE")
    exit()

if(ui=='gui'):
    liblog.write_in_file("WEB INTERFACE SELECTED")
    import web_main as wm
elif(ui=='cli'):
    liblog.write_in_file("COMMAND LINE INTERFACE SELECTED")
    import cli_main as cli
else:
    liblog.write_in_file("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    print("ERROR: USER INTERFACE NOT PROPERLY SET IN THE CONFIG FILE")
    exit()