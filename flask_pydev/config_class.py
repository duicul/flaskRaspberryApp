'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
import json
from multiprocessing.util import LOGGER_NAME

class Config:
    def __init__(self,user_name,url,period):
        self.user_name=user_name
        self.url=url
        self.period=period
        
    def __str__(self):
        return str(self.user_name)+" "+str(self.url)+" "+str(self.period)
    
    def toJSON(self):
        return {"user_name":self.user_name,"url":self.url,"period":self.period}
    
class Config_Data:
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="Config"
        self.create_table()
        if(len(self.getAllConfigs())==0):
           self.addConfig(Config("admin","http://192.168.0.6",900))
    
    def getConfig(self,user_name):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"'"
        mycursor.execute(querry)
        result=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        config = None
        if(len(result)>0):
            config = Config(result[0][1],result[0][2],result[0][3])
        return config
    
    def getAllConfigs(self):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name
        mycursor.execute(querry)
        result=[]
        configs=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        for rec in result:
            configs.append(Config(rec[1],rec[2],rec[3]))
        return configs
    
    def removeConfig(self,user_name):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="DELETE FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"'"
        print(querry)
        try:
            mycursor.execute(querry)
            conn.commit()
            mycursor.close()
            conn.close()
            return True
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return False    
        
    def addConfig(self,config):
        conn = sqlite3.connect(self.database)
        vals=[(config.user_name,config.url,config.period)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (USER_NAME,URL,PERIOD) VALUES (?,?,?)"""
        
        try:
            mycursor.executemany(sql,vals)
            conn.commit()
            mycursor.close()
            conn.close()
            return True
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return False
    
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor=conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS "+self.table_name+" ("
        sql+="ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql+="USER_NAME VARCHAR(32) NOT NULL UNIQUE,"
        sql+="URL VARCHAR(128) NOT NULL,"
        sql+="PERIOD INT NOT NULL);"
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name+" created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
    
    def updateConfig(self,config):
        self.removeConfig(config.user_name)
        self.addConfig(config)
        
class Config_Handler:
    def __init__(self,file_name,logger_name):
        self.file_name=file_name
        self.logger_name=logger_name
        
    def loadUsingFile(self):
        user_name="admin"
        try:
            file=open(self.file_name,"r")
            file_json=json.load(file)
            user_name=file_json["user_name"]
            file.close()
        except:
            file_json={"user_name":"admin"}
            file=open(self.file_name,"w")
            json.dump(file_json,file)
            file.close()
        cd=Config_Data("db/config.db",self.logger_name)
        return cd.getConfig(user_name)

if __name__ == '__main__':
    cd=Config_Data("db/config.db","random")
    cd.create_table()
    cd.removeConfig("admin")
    cd.addConfig(Config("admin","http://192.168.0.6",900))
    for c in cd.getAllConfigs():
        print(c)