'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
import requests
from mailapi import send_mail,read_mail_config

class Table_Data:
    
    def __init___(self,database,home_station_url,logger_name):
        self.database=database
        self.home_station_url=home_station_url
        self.logger_name=logger_name
    
    def create_table(self):
        ''' Create corresponding table '''
        pass
    
    def remove_wrong_value(self):
        ''' Remove incorrect values from the database '''
        pass
    
    def extract_all_interval(self,items):
        ''' Returns last items rows from the table '''
        try:
            items=int(items)
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
            return []
        if(items!=-1):
            condition=" WHERE ID >= ((SELECT MAX(ID)  FROM "+self.table_name+") - "+str(items)+")"
        else:
            condition=""
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extract_last(self):
        """Extracts the latest row from the table"""
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" WHERE ID = (SELECT MAX(ID)  FROM "+self.table_name+")"
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result[0] if len(result)>0 else None
    
    def poll_value(self):
        """ Poll sensor values from the sensor """
        pass
    
class Temperature_Data(Table_Data):
    
    def __init__(self,database,home_station_url,logger_name):
        self.database=database
        self.home_station_url=home_station_url
        self.logger_name=logger_name
        self.table_name="Temperature_Data"
        self.notified_temp=[False,False]
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE "+self.table_name+" ("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        sql+="TEMP1 REAL NOT NULL,"
        sql+="TEMP2 REAL NOT NULL);"
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name+" created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
    
    def remove_wrong_value(self):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        sql = "DELETE FROM "+self.table_name+" WHERE TEMP1 = -127 OR TEMP2 = -127"
        mycursor.execute(sql)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))    
    
    def insert(self,temp1,temp2):
        conn = sqlite3.connect(self.database)
        vals=[(temp1,temp2)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (TEMP1,TEMP2) VALUES (?,?)"""
        mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def poll_value(self):
        i=0
        temp1=-127
        temp2=-127
        while (temp1==-127 or temp2==-127) and i<30:
            i=i+1
            try:
                temp = requests.get(self.home_station_url+"/temperature").json()
            except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return 
            temp1=float(temp["temp1"]) if float(temp["temp1"])!=-127 else temp1
            temp2=float(temp["temp2"]) if float(temp["temp2"])!=-127 else temp2
            
        logging.getLogger(self.logger_name).info(" polled "+str(self.home_station_url)+" result: "+str(temp1)+" "+str(temp2)+" "+str(i)+"tries")
        try:
                mail_config=read_mail_config()
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                
        try:
                if (temp1>int(mail_config["temp1"]["max"]) or temp1<int(mail_config["temp1"]["min"])) and not self.notified_temp[0]:
                        send_mail("Temperatura atinsa : "+str(temp1)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[0]=True
                elif temp1>int(mail_config["temp1"]["min"]) and temp1<int(mail_config["temp1"]["max"]) and self.notified_temp[0]:
                        self.notified_temp[0]=False
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))

        try:
                if (temp2>int(mail_config["temp2"]["max"]) or temp2<int(mail_config["temp2"]["min"])) and not self.notified_temp[1]:
                        send_mail("Temperatura atinsa : "+str(temp2)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[1]=True
                elif temp2>int(mail_config["temp2"]["min"]) and temp2<int(mail_config["temp2"]["max"]) and self.notified_temp[1]:
                        self.notified_temp[1]=False
        except:
                logging.getLogger('monitor_logger').error(str(traceback.format_exc()))
        
        if temp1 != -127 and temp2 != -127:
            self.insert(temp1,temp2)

class Voltage_Data(Table_Data):
    
    def __init__(self,database,home_station_url,logger_name):
        self.database=database
        self.home_station_url=home_station_url
        self.logger_name=logger_name
        self.table_name="Voltage_Data"
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE "+self.table_name+" ("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        sql+="VOLT REAL NOT NULL);"
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name+" created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
    
    def remove_wrong_value(self):
        """"  Not implemented """
        pass
    
    def insert(self,volt):
        conn = sqlite3.connect(self.database)
        vals=[(volt,)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (VOLT) VALUES (?)"""
        mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def poll_value(self):
        try:
            volt = [requests.get(self.home_station_url+"/voltage").json()["volt1"] for i in range(4)]
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return
        volt = sum(volt)/len(volt)
        logging.getLogger('monitor_logger').info(" polled "+str(self.home_station_url)+" result: "+str(volt))
        self.insert(float(volt))
    
if __name__ == '__main__':
    vd=Voltage_Data("measure.db","random","random")
    vd.insert(12.6)
    td=Temperature_Data("measure.db","random","random")
    td.insert(20,30)
    print(td.extract_last())
    print(td.extract_all_interval(2))
    pass