'''
Created on Oct 27, 2020

@author: duicul
'''
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
myCmd = 'mkdir '+BASE_DIR+'/logs;chmod a+w '+BASE_DIR+'/logs;'
os.system(myCmd)
myCmd = 'sudo apt install nginx uwsgi uwsgi-plugin-python3'
os.system(myCmd)
myCmd = 'sudo pip3 install pysha3'
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
import restartServices