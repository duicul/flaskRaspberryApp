'''
Created on Aug 10, 2020

@author: duicul
'''
import requests
import logging
import traceback

class Weather:
    
    def __init__(self,api_key,city,logger_name):
        self.api_key=api_key
        self.city=city
        self.logger_name=logger_name
        
    def request_data(self):
        try:
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q={"+str(self.city)+"}&appid={"+str(self.api_key)+"}")
        except:
            print(str(traceback.format_exc()))
            logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
            return
        json_data=r.json()
        #print(json_data)
        logging.getLogger(self.logger_name).info(str(json_data))
        
if __name__ == '__main__':
    w=Weather("random","random","random")
    w.request_data()