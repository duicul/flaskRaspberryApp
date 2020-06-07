import time
import datetime
import requests
import json
import traceback
from  threading import Thread
import sqlite3
import logging

def clean_table():
    conn = sqlite3.connect('measure.db')
    cursor=conn.cursor()
    try:
        cursor.execute("DROP Table Measure;")
        mydb.commit()
    except Exception:
        now=time.asctime( time.localtime(time.time()) )
        logging.debug(str(now)+str(traceback.format_exc()))
    cursor.close()
    conn.close()
    create_table()
    
def create_table():
        conn = sqlite3.connect('measure.db')
        cursor=conn.cursor()
        sql="CREATE TABLE Measure("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        sql+="TEMP1 REAL NOT NULL,"
        sql+="TEMP2 REAL NOT NULL,"
        sql+="VOLT REAL NOT NULL);"
        try:
            cursor.execute(sql)
            logging.debug('Table created')
            cursor.close()
            conn.close()
        except:
            now=time.asctime(time.localtime(time.time()) )
            logging.warning(str(now)+ str(traceback.format_exc()))

def remove_wrong_value():
        conn = sqlite3.connect('measure.db')
        mycursor=conn.cursor()
        sql = "DELETE FROM Measure WHERE TEMP1 = -127 OR TEMP2 = -127"
        result=mycursor.execute(sql)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            now=time.asctime(str(now)+ time.localtime(time.time()) )
            logging.error(str(traceback.format_exc()))

def insert(temp1,temp2,volt):
        conn = sqlite3.connect('measure.db')
        vals=[(temp1,temp2,volt)]
        #print(vals)
        mycursor=conn.cursor()
        sql = """INSERT INTO Measure (TEMP1,TEMP2,VOLT) VALUES (?,?,?)"""
        initresp = time.time_ns()
        result=mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            now=time.asctime(str(now)+ time.localtime(time.time()) )
            logging.error(str(traceback.format_exc()))

def extract_all_interval(items):
        #print("extract_all_interval")
        try:
            items=int(items)
        except:
            now=time.asctime( time.localtime(time.time()) )
            logging.error(str(now)+str(traceback.format_exc()))
            return []
        if(items!=-1):
            condition=" WHERE ID >= ((SELECT MAX(ID)  FROM Measure) - "+str(items)+")"
        else:
            condition=""
        #print(condition)
        conn = sqlite3.connect('measure.db')
        mycursor=conn.cursor()
        querry="SELECT * FROM Measure "+condition
        #print(querry)
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            now=time.asctime( time.localtime(time.time()) )
            logging.error(str(now)+str(traceback.format_exc()))
        #print(result)
        return result
        
def extract_last():
        conn = sqlite3.connect('measure.db')
        mycursor=conn.cursor()
        querry="SELECT * FROM Measure WHERE ID = (SELECT MAX(ID)  FROM Measure)"
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            now=time.asctime( time.localtime(time.time()) )
            logging.error(str(now)+str(traceback.format_exc()))
        #print(result)
        return result[0] if len(result)>0 else None

def poll_value(home_station_url):
        time_stamp=str(datetime.datetime.now())
        stop=False
        i=0
        temp1=-127
        temp2=-127
        while (temp1==-127 or temp2==-127) and i<30:
            i=i+1
            temp = requests.get(home_station_url+"/temperature").json()
            temp1=float(temp["temp1"]) if float(temp["temp1"])!=-127 else temp1
            temp2=float(temp["temp2"]) if float(temp["temp2"])!=-127 else temp2
        volt = [requests.get(home_station_url+"/voltage").json()["volt1"] for i in range(3)]
        volt=sum(volt)/len(volt)
        if(temp1!=-127 and temp2!=-127):
            insert(temp1,temp2,float(volt))       

class Monitor():
    def __init__(self,home_station_url,period):
        self.home_station_url=home_station_url
        self.period=period
        # Call the Thread class's init function
        Thread.__init__(self)
       
  
    def run(self):
        create_table()
        while True:
            try:
                poll_value(self.home_station_url)
                #extract_all()
                #extract_last()
            except:
                now=time.asctime( time.localtime(time.time()) )
                logging.error(str(now)+str(traceback.format_exc()))
            try:
                file=open("data.json","r")
                file_json=json.load(file)
                file.close()
            except:
                file_json={"url":self.home_station_url,"period":self.period}
                file=open("data.json","w")
                json.dump(file_json,file)
                file.close()
            self.period=file_json["period"]
            self.home_station_url=file_json["url"]
            time.sleep(int(self.period))
        
if __name__ == "__main__":
    try:
        logging.basicConfig(filename='error_monitor.log',level=logging.INFO)
        time.sleep(30)
        mon=Monitor("http://192.168.1.6",1800)
        mon.run()
    except:
        now=time.asctime( time.localtime(time.time()) )
        logging.error(str(now)+str(traceback.format_exc()))
