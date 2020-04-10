import re
import hashlib
from filelock import Timeout, FileLock

class Extractdata_Config:
    def __init__(self,file_name):
        self.file_name=file_name

    def getFile(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            file=open(self.file_name,'r')
            data=file.read()
            file.close()
        return data
    
    def getUsername(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('username=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
        
    def testPassword(self,password):
        m = hashlib.sha256()
        m.update(password.encode())
        t=m.hexdigest()
        filepass=self.getPassword()
        return t==filepass
            
    def getPassword(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('password=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
        
    def getIp(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('ip=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
        
    def getPort(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('port=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''

    def getRefresh_In(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('refresh_in=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''

    def getRefresh_Out(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('refresh_out=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''

    def getLogTime(self):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                found = re.search('logtime=(.*)', data).group(1)
                file.close()
                return found
            except AttributeError:
                file.close()
                return ''
        
class Insertdata_Config:
    def __init__(self,file_name):
        self.file_name=file_name

    def getFile_name(self):
        return self.file_name
    
    def setUsername(self,username):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('username=.*', 'username=%s' % username,data)
                file.write(found)
            except AttributeError as e:
                print(e)
            file.close()
        
    def setPassword(self,password):
        m = hashlib.sha256()
        m.update(password.encode())
        t=m.hexdigest()
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('password=.*', 'password=%s' % t,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()
        
    def setIp(self,ip):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('ip=.*', 'ip=%s' % ip,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()
        
    def setPort(self,port):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('port=.*', 'port=%s' % port,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()

    def setRefresh_In(self,refresh):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('refresh_in=.*', 'refresh_in=%s' % refresh,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()

    def setRefresh_Out(self,refresh):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('refresh_out=.*', 'refresh_out=%s' % refresh,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()

    def setLogTime(self,logtime):
        lock = FileLock(str(self.file_name)+".lock")
        with lock:
            try:
                file=open(self.file_name,'r')
                data=file.read()
                file.close()
                file=open(self.file_name,'w')
                found = re.sub('logtime=.*', 'logtime=%s' % logtime,data)
                file.write(found)
            except AttributeError:
                pass
            file.close()

if __name__ == '__main__':
    ed=Extractdata_Config("../config.txt")
    insd=Insertdata_Config("../config.txt")
    print(ed.getFile())
    insd.setUsername("duicul")
    insd.setPassword("daniel")
    #insd.setIp("31313")
    insd.setPort(6767)
    insd.setRefresh_In(30)
    insd.setRefresh_Out(1)
    insd.setLogTime(20)
    print(ed.testPassword("daniel"))
    print(ed.getUsername())
    print(ed.getPassword())
    print(ed.getIp())
    print(ed.getPort())
    print(ed.getFile())
