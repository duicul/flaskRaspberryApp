'''
Created on Oct 27, 2020

@author: duicul
'''
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

str_out="[uwsgi] \nchdir = "
str_out+=BASE_DIR
str_out+="\n"
str_out+="logto = "+BASE_DIR+"/logs/flaskRaspPi-uwsgi.log\n"
str_out+="plugins = python3\n"
str_out+="module=flask_pydev.wsgi:app\n"
str_out+="wsgi-file = "+BASE_DIR+"/wsgi.py # customize with the relative path to your wsgi.py file \n"

str_out+="workers = 1"
f = open("/etc/uwsgi/apps-enabled/flaskRaspPi.ini", "w")
f.write(str_out)
f.close()
myCmd = 'service uwsgi restart'
os.system(myCmd)