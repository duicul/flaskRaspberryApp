import requests
import json
import time

def showdata():
	r = requests.post('http://192.168.1.38:8765/outputpins',"outputpins")
	return r.text
