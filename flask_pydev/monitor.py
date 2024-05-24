import time
import json
import traceback
from  threading import Thread
import logging
from data_classes import Temperature_Data,Voltage_Data,AC_Data,\
    Temperature_Split_Data,Outside_Data
from data_classes_powmr import PowMr_Data
from config_class import Config_Data

from config_class import Config_Handler
from multiprocessing.util import LOGGER_NAME

class Monitor():
    def __init__(self,user_name,logger_name):
        self.logger_name=logger_name
        self.user_name=user_name
        self.config_handler=Config_Handler("json/monitor_config.json",self.logger_name)
        self.config=self.config_handler.loadUsingFile()
        print("config "+str(config))
        logging.getLogger(self.logger_name).info("Monitor config "+json.dumps(config.toJSON())
        self.url=self.config.url
        self.url_powmr=self.config.url_powmr
        self.period=self.config.period
        # Call the Thread class's init function
        Thread.__init__(self)
  
    def run(self):
        td=Temperature_Split_Data("db/measure.db",self.logger_name)
        vd=Voltage_Data("db/measure.db",self.logger_name)
        acd=AC_Data("db/measure.db",self.logger_name)
        od=Outside_Data("db/measure.db",self.logger_name)
        pmd=PowMr_Data("db/measure_powmr.db",self.logger_name)
        while True:                
            try:
                logging.getLogger(self.logger_name).info("Polling homestation")
                td.poll_value(self.url)
                vd.poll_value(self.url)
                acd.poll_value(self.url)
                od.poll_value()
            except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
            try:
                logging.getLogger(self.logger_name).info("Polling powmr")
                pmd.poll_value(self.url_powmr,mock=False)
            except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
            time.sleep(int(self.period))

def start():
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error_monitor.log',
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    ch = Config_Handler("json/monitor_config.json",'monitor_logger')
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
    print("Monitor start")
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error_monitor.log',
        backupCount=20,
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    ch = Config_Handler("json/monitor_config.json",'monitor_logger')
    config = ch.loadUsingFile()
    print(config.toJSON())
    #mail_config=read_mail_config()
    #logging.getLogger('monitor_logger').info(str(mail_config))
    try:
        logging.getLogger('monitor_logger').info("start")
        mon=Monitor(config.user_name,"monitor_logger")
        mon.run()
    except:
        logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
