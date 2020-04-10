from gpiozero import LED
from time import sleep
import Adafruit_DHT
print("Leds loaded")
def turnon(pin):
	LED(pin).on()

def turnoff(pin):
	LED(pin).off()

def read_temp(pin):
	sensor = Adafruit_DHT.DHT11
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	print(str(humidity)+"  "+str(temperature))
