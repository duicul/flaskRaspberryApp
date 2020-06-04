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
        logging.debug(str(traceback.format_exc()))
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
            logging.warning(str(traceback.format_exc()))
        

def insert(temp1,temp2,volt):
        conn = sqlite3.connect('measure.db')
        vals=[(temp1,temp2,volt)]
        print(vals)
        mycursor=conn.cursor()
        sql = """INSERT INTO Measure (TEMP1,TEMP2,VOLT) VALUES (?,?,?)"""
        initresp = time.time_ns()
        result=mycursor.executemany(sql,vals)
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.error(str(traceback.format_exc()))

def extract_all():
        conn = sqlite3.connect('measure.db')
        mycursor=conn.cursor()
        querry="SELECT * FROM Measure"
        mycursor.execute(querry)
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.error(str(traceback.format_exc()))
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
            logging.error(str(traceback.format_exc()))
        #print(result)
        return result[0] if len(result)>0 else None

def poll_value(home_station_url):
        time_stamp=str(datetime.datetime.now())
        temp = requests.get(home_station_url+"/temperature").json()
        volt = [requests.get(home_station_url+"/voltage").json()["volt1"] for i in range(3)]
        volt=sum(volt)/len(volt)
        insert(float(temp["temp1"]),float(temp["temp2"]),float(volt))       

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
                extract_all()
                extract_last()
            except:
                logging.error(str(traceback.format_exc()))
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
    mon=Monitor("http://192.168.1.6",1800)
    mon.run()
