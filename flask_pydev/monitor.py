import time
import json
import traceback
from  threading import Thread
import logging
from data_classes import Temperature_Data,Voltage_Data,AC_Data,\
    Temperature_Split_Data,Outside_Data
from config_class import Config_Data

from config_class import Config_Handler

class Monitor():
    def __init__(self,user_name,logger_name):
        self.user_name=user_name
        self.config_data=Config_Data("config.db",logger_name)
        self.config=self.config_data.getConfig(user_name)
        self.url=self.config.url
        self.period=self.config.period
        # Call the Thread class's init function
        Thread.__init__(self)
       
    def reset_config(self):
        file_json={"url":self.home_station_url,"period":self.period}
        file=open("data.json","w")
        json.dump(file_json,file)
        file.close()
  
    def run(self):
        td=Temperature_Split_Data("measure.db",self.home_station_url,'monitor_logger')
        vd=Voltage_Data("measure.db",self.home_station_url,'monitor_logger')
        acd=AC_Data("measure.db",self.home_station_url,'monitor_logger')
        od=Outside_Data("measure.db",self.home_station_url,'monitor_logger')
        while True:
            try:
                file=open("data.json","r")
                file_json=json.load(file)
                file.close()
            except:
                self.reset_config()
                
            try:
                
                td.change_url(self.home_station_url)
                vd.change_url(self.home_station_url)
                acd.change_url(self.home_station_url)
                od.change_url(self.home_station_url)
                
                td.poll_value()
                vd.poll_value()
                acd.poll_value()
                od.poll_value()
                
            except:
                logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
            
            try:
                self.period=file_json["period"]
                self.home_station_url=file_json["url"]
            except:
                self.reset_config()
            time.sleep(int(self.period))

def start():
    #import logging
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error_monitor.log',
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    #mail_config=read_mail_config()
    #logging.getLogger('monitor_logger').info(str(mail_config))
    ch = Config_Handler("monitor_config.json",'monitor_logger')
    config = ch.loadUsingFile()
    try:
        logging.getLogger('monitor_logger').info("start")
        time.sleep(30)
        mon=Monitor(config.user_name,"monitor_logger")
        mon.run()
    except:
        logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
     
if __name__ == "__main__":
    #import logging
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error_monitor.log',
        backupCount=20,
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    ch = Config_Handler("monitor_config.json",'monitor_logger')
    config = ch.loadUsingFile()
    #mail_config=read_mail_config()
    #logging.getLogger('monitor_logger').info(str(mail_config))
    try:
        logging.getLogger('monitor_logger').info("start")
        time.sleep(30)
        mon=Monitor(config.user_name,"monitor_logger")
        mon.run()
    except:
        logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
    '''
   from logging.config import dictConfig

    dictConfig({
            'version': 1,
            'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }},
            'handlers': {'wsgi': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'error_monitor.log',
                'maxBytes' :1024 * 1024,
                'backupCount' : 20,
                'formatter': 'default'
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
                    }
                })'''
