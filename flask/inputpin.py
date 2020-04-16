import sys
import Adafruit_DHT
import json

class InputPin:
    
    def __init__(self,pin,sensor_type):
        self.pin=pin
        self.sensor_type=sensor_type

    def show_sensor_data(self):
        if self.sensor_type == "DHT11":
            return self.readDHT11()
        elif self.sensor_type == "DHT11":
            return self.readDHT22()
        elif self.sensor_type == "dummy":
            return [{"name":"dummy_sensor","val":self.pin}]
        else:
            return [{"name":"Sensor type unknown","val":"0"}]
            
    def convert_to_gauge(self,sensor_values):
        ret="<div>"
        for val in sensor_values:
            ret+=str(val["name"])+" = "+str(val["val"])+"</br>"
        ret+="</div>"
        return ret
        
    def readDHT11(self):
        sensor=Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return [{"name":"temperature","val":temperature},{"name":"humidity","val":humidity}]

    def readDHT22(self):
        sensor=Adafruit_DHT.DHT22
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return [{"name":"temperature","val":temperature},{"name":"humidity","val":humidity}]
