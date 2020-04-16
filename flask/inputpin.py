import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
from extractvalues import Extractdata_Config
import json
import requests
from pinconfig import pin_to_GPIO

class InputPin:
    
    def __init__(self,pin,sensor_type):
        self.pin=pin
        self.sensor_type=sensor_type

    def show_gauge(self):
        if sensor_type == "DHT11":
            return convert_to_gauge(self.readDHT11())
        elif sensor_type == "DHT11":
            return convert_to_gauge(self.readDHT22())
        elif sensor_type == "dummy":
            return convert_to_gauge([{name:"dummy_sensor",val:"random"}])
        else:
            return "Sensor type unknown"
            
    def convert_to_gauge(self,sensor_values):
        ret="<div>"
        for val in sensor_values:
            ret+=str(val["name"])+" = "+str(val["val"])+"</br>"
        ret+="</div>"
        return ret
        
    def readDHT11(self):
        sensor=Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return [{name:"temperature",val:temperature},{name:"humidity",val:humidity}]

    def readDHT22(self):
        sensor=Adafruit_DHT.DHT22
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return [{name:"temperature",val:temperature},{name:"humidity",val:humidity}]
