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
            req_url="http://api.weatherapi.com/v1/current.json?key="+str(self.api_key)+"&q="+str(self.city)+"&aqi=no"
            r = requests.get(req_url)
            #print(req_url)
        except:
            #print(str(traceback.format_exc()))
            logging.getLogger( self.logger_name).error(str(traceback.format_exc()))
            return
        json_data=r.json()
        #print(json_data)
        logging.getLogger(self.logger_name).info(str(json_data))
        return json_data
        
if __name__ == '__main__':
    w=Weather("random","random","random")
    w.request_data()