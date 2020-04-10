from extractvalues import Extractdata_Config
from extractvalues import Insertdata_Config
def getconfigdata(filepath):
    ed=Extractdata_Config(filepath)
    data=""
    data = data +"<div class=\"row\"><div class=\"col-3\">Server IP: </div>"+"<div class=\"col-3\"><input id=\"ip\" type=\"text\" value=\""+str(ed.getIp())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Server Port: </div>"+"<div class=\"col-3\"><input id=\"port\" type=\"text\" value=\""+str(ed.getPort())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Refresh rate input pins (s): </div>"+"<div class=\"col-3\"><input id=\"refresh_in\" type=\"text\" value=\""+str(ed.getRefresh_In())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Refresh rate output pins (s): </div>"+"<div class=\"col-3\"><input id=\"refresh_out\" type=\"text\" value=\""+str(ed.getRefresh_Out())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Input pins logging time (min): </div>"+"<div class=\"col-3\"><input id=\"logtime\" type=\"text\" value=\""+str(ed.getLogTime())+"\"> </div></div>"
    data = data
    return data

def getpassworddata(filepath):
    ed=Extractdata_Config(filepath)
    data=""
    data = data +"<div class=\"row\"><div class=\"col-3\">Username: </div>"+"<div class=\"col-3\"><input id=\"username\" type=\"text\" value=\""+str(ed.getUsername())+"\"> </div></div>"
    data = data +"<div class=\"row\"><div class=\"col-3\">Password: </div>"+"<div class=\"col-3\"><input id=\"password\" type=\"password\" value=\"\"> </div></div>"
    return data

def setconfigdata(filepath,username,password,ip,port,refresh_in,refresh_out,logtime):
    print("setconfigcall")
    insd=Insertdata_Config(filepath)
    print("setting config values")
    insd.setUsername(username)
    insd.setPassword(password)
    insd.setIp(ip)
    insd.setPort(port)
    insd.setRefresh_In(refresh_in)
    insd.setRefresh_Out(refresh_out)
    insd.setLogTime(logtime)

def setpassword(filepath,username,password):
    print("setconfigcall")
    insd=Insertdata_Config(filepath)
    print("setting config values")
    insd.setUsername(username)
    insd.setPassword(password)
