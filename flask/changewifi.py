import re
from filelock import Timeout, FileLock

class Extractdata_Wifi:
    def __init__(self,file_name):
        self.file_name=file_name

    def getFile(self):
        lock = FileLock("wifiaux.lock")
        with lock:
            file=open(self.file_name,'r')
            data=file.read()
            file.close()
        return data
    
    def getSSID(self):
        lock = FileLock("wifiaux.lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('ssid=\"(.*)\"', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
            
    def getPsk(self):
        lock = FileLock("wifiaux.lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('psk=\"(.*)\"', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
        
class Insertdata_Wifi:
    def __init__(self,file_name):
        self.file_name=file_name

    def getFile_name(self):
        return self.file_name

    def writeconf_file(self):
        lock = FileLock("wifiaux.lock")
        with lock:
            file=open(self.file_name,'w+')
            f = "country=ro \n update_config=1 \n ctrl_interface=/var/run/wpa_supplicant\n\nnetwork={\n scan_ssid=1\n ssid=\"MyNetworkSSID\"\n psk=\"Pa55w0rd1234\"\n}"
            file.write(f)
            file.close()
    
    def setSSID(self,ssid):
        lock = FileLock("wifiaux.lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('ssid=\".*\"', 'ssid=\"%s\"' % ssid,data)
                file.write(found)
            except AttributeError as e:
                print(e)
            file.close()
        
        
    def setPsk(self,psk):
        lock = FileLock("wifiaux.lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('psk=\".*\"', 'psk=\"%s\"' % psk,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()
        
if __name__ == '__main__':
    ed=Extractdata_Wifi("../wpa_supplicant.conf")
    insd=Insertdata_Wifi("../wpa_supplicant.conf")
    print(ed.getFile())
    insd.setSSID("Tenda_962970")
    insd.setPsk("pufulete")
    print(ed.getSSID())
    print(ed.getPsk())
    #insd.writeconf_file()

