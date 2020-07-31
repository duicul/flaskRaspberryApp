import time
import json
import traceback
from  threading import Thread
import logging
from data_classes import Temperature_Data,Voltage_Data

class Monitor():
    def __init__(self,home_station_url,period):
        self.home_station_url=home_station_url
        self.period=period
        # Call the Thread class's init function
        Thread.__init__(self)
       
  
    def run(self):
        td=Temperature_Data("measure.db",self.home_station_url,'monitor_logger')
        vd=Voltage_Data("measure.db",self.home_station_url,'monitor_logger')
        while True:
            try:
                file=open("data.json","r")
                file_json=json.load(file)
                file.close()
            except:
                file_json={"url":self.home_station_url,"period":self.period}
                file=open("data.json","w")
                json.dump(file_json,file)
                file.close()
                
            try:
                
                td.change_url(self.home_station_url)
                vd.change_url(self.home_station_url)
                
                td.poll_value()
                vd.poll_value()

            except:
                logging.getLogger('monitor_logger').error(str(traceback.format_exc()))

            self.period=file_json["period"]
            self.home_station_url=file_json["url"]
            time.sleep(int(self.period))
        
if __name__ == "__main__":
    #import logging
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'error_monitor.log',
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    #mail_config=read_mail_config()
    #logging.getLogger('monitor_logger').info(str(mail_config))
    
    try:
        logging.getLogger('monitor_logger').info("start")
        time.sleep(30)
        mon=Monitor("http://192.168.1.6",900)
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
                'class': 'logging.FileHandler',
                'filename': 'error_monitor.log',
                'formatter': 'default'
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
                    }
                })'''
