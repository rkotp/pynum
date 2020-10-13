import xml.etree.ElementTree as ET
import pathlib

def get_dbg():

    # READ CONFIGURATION FILE
    xml_file = str(pathlib.Path(__file__).parent.parent.absolute()) + "/config.xml"
    xmlTree = ET.parse(xml_file)
    rootElement = xmlTree.getroot()

    # GET THE DEBUG MODE
    debug_aux = rootElement.findall("./debug_mode")

    # CHECK IF IT IS PROPERLY SET
    if (not(len(debug_aux)==1)):
        return [-1,'']
    pynum_debug = debug_aux[0].text
    if (not( pynum_debug=='yes' or pynum_debug=='no' )):
        return [-1,'']

    # SET THE RETURNED VALUE
    if ( pynum_debug == 'no' ):
        return [0,False]
    elif ( pynum_debug == 'yes' ):
        return [0,True]