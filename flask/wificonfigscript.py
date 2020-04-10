from changewifi import Extractdata_Wifi
from changewifi import Insertdata_Wifi
def getwifidata(filepath):
    ed=Extractdata_Wifi(filepath)
    data=""
    data = data +"<div class=\"row\"><div class=\"col-3\">SSID: </div>"+"<div class=\"col-3\"><input id=\"wifi_ssid\" type=\"text\" value=\""+str(ed.getSSID())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Psk: </div>"+"<div class=\"col-3\"><input id=\"wifi_psk\" type=\"password\" value=\""+str(ed.getPsk())+"\"> </div></div>"
    data = data
    return data

def setwifidata(filepath,ssid,psk):
    insd=Insertdata_Wifi(filepath)
    insd.writeconf_file()
    print("setwificall")
    print("setting wifi values")
    insd.setSSID(ssid)
    insd.setPsk(psk)

    
if __name__ == '__main__':
    print(getwifidata("../wpa_supplicant.conf"))
    setwifidata("../wpa_supplicant.conf","admin","pass")
    '''ed=Extractdata_Wifi("../wpa_supplicant.conf")
    insd=Insertdata_Wifi("../wpa_supplicant.conf")
    print(ed.getFile())
    insd.setSSID("Tenda_962970")
    insd.setPsk("pufulete")
    print(ed.getSSID())
    print(ed.getPsk())
    #insd.writeconf_file()'''

