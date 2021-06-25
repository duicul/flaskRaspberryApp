'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
import requests
from mailapi import send_mail,read_mail_config
from weather import Weather
import json 

class Table_Data:
    
    def __init___(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
    
    def current_timestamp(self):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT datetime('now','localtime') "
        mycursor.execute(querry)
        result=""
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result   
    
    def create_table(self):
        ''' Create corresponding table '''
        pass
    
    def remove_wrong_value(self):
        ''' Remove incorrect values from the database '''
        pass
    
    def extract_all_between(self,fdate,ldate):
        condition=" WHERE date(TIMESTAMP) BETWEEN '"+str(fdate)+"' AND  '"+str(ldate)+"' ;"
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition
        logging.info(querry)
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extractCompare(self,date1,date2):
        condition=" WHERE date(TIMESTAMP) ='"+str(date1)+"' OR  date(TIMESTAMP)='"+str(date2)+"' ;"
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition
        logging.info(querry)
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extract_all_interval(self,items):
        ''' Returns last items rows from the table '''
        condition=""
        #print(items)
        if items=="0":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','0 days' ,'localtime') AND  date('now','localtime') "
        elif items=="1":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-1 days' ,'localtime') AND  date('now','localtime') "
        elif items=="2":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-2 days' ,'localtime') AND  date('now','localtime') "
        elif items=="3":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-3 days' ,'localtime') AND  date('now','localtime') "
        elif items=="4":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-4 days' ,'localtime') AND  date('now','localtime') "
        elif items=="5":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-5 days','localtime') AND  date('now','localtime') "
        elif items=="6":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-6 days' ,'localtime') AND  date('now','localtime') "  
        elif items=="7":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-7 days' ,'localtime') AND  date('now','localtime') "
        elif items=="8":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-8 days' ,'localtime') AND  date('now','localtime') "
        elif items=="9":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-9 days' ,'localtime') AND  date('now','localtime') "
        elif items=="10":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-10 days','localtime' ) AND  date('now','localtime') "
        elif items=="1m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','localtime') AND  date('now','localtime') "    
        elif items=="2m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-1 month','localtime') AND  date('now','localtime') "
            #condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-2 months' ) AND  date('now') "
        elif items=="3m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-2 month','localtime') AND  date('now','localtime') "                
        #try:
        #    items=int(items)
        #except:
        #    logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        #    return []
        #logging.getLogger(self.logger_name).info(condition)
        #print(condition)
        #if(items!=-1):
        #    condition=querry #" WHERE ID >= ((SELECT MAX(ID)  FROM "+self.table_name+") - "+str(items)+")"
        #else:
        #    condition=""
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition
        logging.getLogger(self.logger_name).info(querry)
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
    
    def restart_device(self,home_station_url):
        logging.getLogger(self.logger_name).info("Restart")
        requests.get(home_station_url+"/restart")
    
class Temperature_Data(Table_Data):
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="Temperature_Data"
        self.notified_temp=[False,False]
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS "+self.table_name+" ("
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
    
    def poll_value(self,home_station_url):
        i=0
        temp1=-127
        temp2=-127
        while (temp1==-127 or temp2==-127) and i<30:
            i=i+1
            try:
                temp = requests.get(home_station_url+"/temperature").json()
            except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return 
            temp1=float(temp["temp1"]) if float(temp["temp1"])!=-127 else temp1
            temp2=float(temp["temp2"]) if float(temp["temp2"])!=-127 else temp2
            
        logging.getLogger(self.logger_name).info(" polled temperature"+str(home_station_url)+" result: "+str(temp1)+" "+str(temp2)+" "+str(i)+"tries")
        try:
                mail_config=read_mail_config()
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        
        if temp1 != -127 or temp2 != -127:
            self.insert(temp1,temp2)
            self.restart_device()
        elif temp1==-127 and temp2==-127:
            self.restart_device()
            return
                
        try:    
                if(temp1!=-127):
                    if (temp1>int(mail_config["temp1"]["max"]) or temp1<int(mail_config["temp1"]["min"])) and not self.notified_temp[0]:
                        send_mail("Temperatura atinsa : "+str(temp1)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[0]=True
                    elif temp1>int(mail_config["temp1"]["min"]) and temp1<int(mail_config["temp1"]["max"]) and self.notified_temp[0]:
                        self.notified_temp[0]=False
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))

        try:
                if(temp2!=-127):
                    if (temp2>int(mail_config["temp2"]["max"]) or temp2<int(mail_config["temp2"]["min"])) and not self.notified_temp[1]:
                        send_mail("Temperatura atinsa : "+str(temp2)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[1]=True
                    elif temp2>int(mail_config["temp2"]["min"]) and temp2<int(mail_config["temp2"]["max"]) and self.notified_temp[1]:
                        self.notified_temp[1]=False
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        
        

class Voltage_Data(Table_Data):
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="Voltage_Data"
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS "+self.table_name+" ("
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
    
    def poll_value(self,home_station_url):
        try:
            volt = [requests.get(home_station_url+"/voltage").json()["volt1"] for i in range(4)]
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return
        volt = round(sum(volt)/len(volt),2)
        logging.getLogger(self.logger_name).info(" polled voltage "+str(home_station_url)+" result: "+str(volt))
        self.insert(float(volt))

class AC_Data(Table_Data):
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="AC_Data"
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS "+self.table_name+" ("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        sql+="VOLT REAL NOT NULL,"
        sql+="CURRENT REAL NOT NULL,"
        sql+="POWER REAL NOT NULL,"
        sql+="ENERGY REAL NOT NULL);"
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
        sql = "DELETE FROM "+self.table_name+" WHERE ENERGY = '-1' "
        mycursor.execute(sql)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def insert(self,volt,current,power,energy):
        conn = sqlite3.connect(self.database)
        vals=[(volt,current,power,energy)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (VOLT,CURRENT,POWER,ENERGY) VALUES (?,?,?,?)"""
        mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def poll_value(self,home_station_url):
        try:
            ac = [requests.get(home_station_url+"/ac").json() for i in range(4)]
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return
        volt = round(sum([ac[i]["voltage"] for i in range(len(ac))])/len(ac),2)
        current = round(sum([ac[i]["current"] for i in range(len(ac))])/len(ac),2)
        power = round(sum([ac[i]["power"] for i in range(len(ac))])/len(ac),2)
        energy = ac[len(ac)-1]["energy"]
        logging.getLogger(self.logger_name).info(" polled AC "+str(home_station_url)+" result: "+str(volt)+" "+str(current)+" "+str(power)+" "+str(energy))
        self.remove_wrong_value()
        if(float(energy)==0):
            self.restart_device()
        else:
            self.insert(float(volt),float(current),float(power),float(energy))

class Temperature_Split_Data(Table_Data):
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="Temperature_Split_Data"
        self.notified_temp=[False,False]
        self.create_table()
       
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS "+self.table_name+" ("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        sql+="TEMP_ID INTEGER NOT NULL , "
        sql+="TEMP REAL NOT NULL, "
        sql+="UNIQUE(TIMESTAMP,TEMP_ID));"
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
        sql = "DELETE FROM "+self.table_name+" WHERE TEMP=-127 OR TEMP_ID >5"
        mycursor.execute(sql)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))    
    
    def insert(self,temp,temp_id,timestamp=None):
        conn = sqlite3.connect(self.database)
        vals=[(temp,temp_id)] if timestamp==None else [(temp,temp_id,timestamp)]
        mycursor=conn.cursor()
        timestamp_string="" if timestamp==None else " , TIMESTAMP "
        sql = """INSERT INTO """+self.table_name+""" (TEMP,TEMP_ID"""+timestamp_string+""") VALUES (?,?"""+("" if timestamp==None else ",?")+""")"""
        print(sql)
        mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def convert_old(self):
        td=Temperature_Data(self.database,self.logger_name)
        for temp_rec in td.extract_all_interval(""):
            self.insert(1,temp_rec[2], temp_rec[1])
            self.insert(2,temp_rec[3], temp_rec[1])
    
    def poll_value(self,home_station_url):
        i=0
        temp1=-127
        temp2=-127
        self.remove_wrong_value()
        while (temp1==-127 or temp2==-127) and i<30:
            i=i+1
            try:
                temp = requests.get(home_station_url+"/temperature").json()
            except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return 
            temp1=float(temp["temp1"]) if float(temp["temp1"])!=-127 else temp1
            temp2=float(temp["temp2"]) if float(temp["temp2"])!=-127 else temp2
            
        logging.getLogger(self.logger_name).info("Temperature_Split_Data polled temperature"+str(home_station_url)+" result: "+str(temp1)+" "+str(temp2)+" "+str(i)+"tries")
        try:
                mail_config=read_mail_config()
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        
        if temp1 != -127:
            self.insert(temp1,1)
        if temp2 != -127:
            self.insert(temp2,2)
                            
        try:    
                if(temp1!=-127):
                    if (temp1>int(mail_config["temp1"]["max"]) or temp1<int(mail_config["temp1"]["min"])) and not self.notified_temp[0]:
                        send_mail("Temperatura atinsa : "+str(temp1)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[0]=True
                    elif temp1>int(mail_config["temp1"]["min"]) and temp1<int(mail_config["temp1"]["max"]) and self.notified_temp[0]:
                        self.notified_temp[0]=False
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))

        try:
                if(temp2!=-127):
                    if (temp2>int(mail_config["temp2"]["max"]) or temp2<int(mail_config["temp2"]["min"])) and not self.notified_temp[1]:
                        send_mail("Temperatura atinsa : "+str(temp2)+"C")
                        logging.getLogger(self.logger_name).info("Temperatura atinsa : "+str(temp1)+"C")
                        self.notified_temp[1]=True
                    elif temp2>int(mail_config["temp2"]["min"]) and temp2<int(mail_config["temp2"]["max"]) and self.notified_temp[1]:
                        self.notified_temp[1]=False
        except:
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def extract_all_between(self,fdate,ldate):
        condition=" WHERE date(TIMESTAMP) BETWEEN '"+str(fdate)+"' AND  '"+str(ldate)+"' and TEMP!=-127 ;"
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition
        logging.info(querry)
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extract_all_interval(self,items):
        ''' Returns last items rows from the table '''
        condition=""
        #print(items)
        if items=="0":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','0 days' ,'localtime') AND  date('now','localtime') "
        elif items=="1":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-1 days' ,'localtime') AND  date('now','localtime') "
        elif items=="2":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-2 days' ,'localtime') AND  date('now','localtime') "
        elif items=="3":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-3 days' ,'localtime') AND  date('now','localtime') "
        elif items=="4":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-4 days' ,'localtime') AND  date('now','localtime') "
        elif items=="5":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-5 days','localtime') AND  date('now','localtime') "
        elif items=="6":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-6 days' ,'localtime') AND  date('now','localtime') "  
        elif items=="7":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-7 days' ,'localtime') AND  date('now','localtime') "
        elif items=="8":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-8 days' ,'localtime') AND  date('now','localtime') "
        elif items=="9":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-9 days' ,'localtime') AND  date('now','localtime') "
        elif items=="10":
            condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-10 days','localtime' ) AND  date('now','localtime') "
        elif items=="1m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','localtime') AND  date('now','localtime') "    
        elif items=="2m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-1 month','localtime') AND  date('now','localtime') "
            #condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-2 months' ) AND  date('now') "
        elif items=="3m":
            condition=" WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-2 month','localtime') AND  date('now','localtime') "                
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" "+condition+" AND TEMP!=-127"
        logging.getLogger(self.logger_name).info(querry)
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
        querry="SELECT ID,MAX(TIMESTAMP),TEMP_ID,TEMP FROM Temperature_Split_Data WHERE TEMP!=-127 GROUP BY TEMP_ID;"
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        ret_val=[]
        for rec in result:
            ret_val.append({"date":rec[1],"temp_id":rec[2],"temp":rec[3]})
        
        return ret_val

class Outside_Data(Temperature_Split_Data):
    
    def poll_value(self):
        city=""
        api_key=""
        try:
            file=open("config_weather.json","r")
            file_json=json.load(file)
            file.close()
            city=file_json["city"]
            api_key=file_json["api_key"]
        except:
            file_json={"api_key":"random","city":"random"}
            file=open("config_weather.json","w")
            json.dump(file_json,file)
            file.close()
        
        weat=Weather(api_key,city,'werkzeug')
        data=weat.request_data()
        try:
            temp=data["main"]["temp"]
            humid=data["main"]["humidity"]
            wind_speed=data["wind"]["speed"]
            logging.getLogger(self.logger_name).info("Outside_Data polled "+" result: "+str(temp)+" "+str(humid))
            if temp!=None:
                self.insert(temp, 3)
            if humid!=None:
                self.insert(humid, 4)
            if wind_speed!=None:
                self.insert(wind_speed, 5)
        except:
            pass
        return data
        
if __name__ == '__main__':
    #ac=AC_Data("measure.db","random","random")
    #ac.insert(221,6.3,170,5478)
    tsd=Temperature_Split_Data("measure.db","random","random")
    tsd.create_table()
    #tsd.insert(1,42.3)
    print(tsd.extract_all_interval(""))
    #tsd.convert_old()
    #td.insert(20,30)
    #print(ac.extract_last())
    #print(ac.extract_all_interval(2))
    pass