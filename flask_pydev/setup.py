'''
Created on Oct 27, 2020

@author: duicul
'''
import os
import json
import restartServices
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
myCmd = 'mkdir '+BASE_DIR+'/logs;chmod a+w '+BASE_DIR+'/logs;'
os.system(myCmd)
myCmd = 'sudo apt install nginx uwsgi uwsgi-plugin-python3'
os.system(myCmd)
myCmd = 'sudo pip3 install pysha3'
os.system(myCmd)
myCmd = 'sudo pip3 install flask-login'
os.system(myCmd)
myCmd = 'chmod a+w .'
os.system(myCmd)
myCmd = 'chmod a+w ..'
os.system(myCmd)
myCmd = 'chmod a+w logs'
os.system(myCmd)
import Createuwsgiconfig
import Createnginxconfig
myCmd = 'chmod a+w ./*'
os.system(myCmd)
myCmd = 'chmod a+w ../*'
os.system(myCmd)
print("Weather settings: ")
skip1=input("Skip? yes/no")
if(not(len(skip1)>0 and (skip1[0]=='y' or skip1[0]=='Y'))):
    api_key = input("api_key: ")
    city = input("city: ")
    file_json={"api_key":api_key,"city":city}
    file=open("config_weather.json","w")
    json.dump(file_json,file)
    file.close()
    
print("Mail settings: ")
skip2=input("Skip? yes/no")
if(not(len(skip2)>0 and (skip2[0]=='y' or skip2[0]=='Y'))):
    temp1min = int(input("Temperature 1 Min"))
    temp1max = int(input("Temperature 1 Max"))
    temp2min = int(input("Temperature 2 Min"))
    temp2max = int(input("Temperature 2 Max"))    
    print("Mail Account: ")
    username = input("Username: ")
    mail = input("Mail: ")
    password = input("Password: ")
    norec = int(input("Number of receivers: "))
    recs = []
    for i in range(norec):
        rec = input("Receiver mail: ")
        recs.append(rec)    
    {"temp1":{"min":temp1min,"max":temp1max},"temp2":{"min":temp2min,"max":temp2max},"mail_account":{"user":username,"mail":mail,"pass":password},"receivers":recs}
    file=open("mailconfig.json","w")
    json.dump(file_json,file)
    file.close()
restartServices.run()
