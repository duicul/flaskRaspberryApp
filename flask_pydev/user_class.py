'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
from flask_login import UserMixin,AnonymousUserMixin
import time
from datetime import datetime, timedelta
from matplotlib.dates import hours

class User(UserMixin):
    def __init__(self,user_name,password,mail):
        self.user_name=user_name
        self.password=password
        self.mail=mail
        self.attempts = 0
        
    def __str__(self):
        return str(self.user_name)+" "+str(self.password)+" "+str(self.mail)
    
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.user_name
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal
    
    def increaseAttempts(self):
        pass
        
    def countReached(self):
        return False

class UserAnonym(AnonymousUserMixin):
    def __init__(self,attempts=0):
        self.attempts=attempts
        self.max_attemps=5
        
    def __str__(self):
        return str(self.attempts)+" "+str(self.countReached())
    
    def increaseAttempts(self):
        self.attempts+=1
        
    def countReached(self):
        return self.attempts>self.max_attemps
   
class User_Data:
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="User"
        self.create_table()
        self.login_data=LoginAttempt_Data("loginattempt.db",logger_name)
        self.attempt_period=timedelta(hours=4)
        
    def getUser(self,user_name):
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
        user = None
        if(len(result)>0):
            user = User(result[0][1],result[0][2],result[0][3])
        if(user==None):
            fromtime=datetime.now()-timedelta(minutes=30)
            epochtime=time.mktime(fromtime.timetuple())
            logins = len(filter(lambda logatt:not logatt.success,self.login_data.getAllAttemptsUser(user_name, epochtime)))
            user = UserAnonym(len(logins))
        return user
    
    def loginUser(self,user_name,password,ip,epochtime):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"' AND PASSWORD='"+password+"'"
        mycursor.execute(querry)
        result=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        user = None
        if(len(result)>0):
            user = User(result[0][1],result[0][2],result[0][3])
        if(user==None):
            fromtime=datetime.now()-timedelta(minutes=30)
            epochtime=time.mktime(fromtime.timetuple())
            logins = len(list(filter(lambda logatt:not logatt.success,self.login_data.getAllAttemptsIp(ip, epochtime))))
            return UserAnonym(logins)
        else:
            logins = len(list(filter(lambda logatt:not logatt.success,self.login_data.getAllAttemptsIp(ip, epochtime))))
            if(logins>5):
                return UserAnonym(logins)
        return user
    
    def getAllUsers(self):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name
        mycursor.execute(querry)
        result=[]
        users=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        user = None
        for rec in result:
            users.append(User(rec[1],rec[2],rec[3]))
        return users
    
    def removeUser(self,user_name):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="DELETE FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"'"
        
        try:
            mycursor.execute(querry)
            conn.commit()
            mycursor.close()
            conn.close()
            return True
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return False    
        
    def addUser(self,user):
        conn = sqlite3.connect(self.database)
        vals=[(user.user_name,user.password,user.mail)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (USER_NAME,PASSWORD,MAIL) VALUES (?,?,?)"""
        
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
        sql+="PASSWORD VARCHAR(128) NOT NULL,"
        sql+="MAIL VARCHAR(32) NOT NULL);"
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name+" created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))

class LoginAttempt:
    def __init__(self,user_name,ip,time_stamp,success):
        self.user_name=user_name
        self.ip=ip
        self.time_stamp=time_stamp
        self.success=True if success == 1 else False
    
    def toJSON(self):
        return {"user_name":self.user_name,"ip":self.ip,"time_stamp":self.time_stamp,"success":self.success}
    
class LoginAttempt_Data:
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="LoginAttempt"
        self.create_table()
    
    def getLastLoginAttempt(self,user_name):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="SELECT * FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"' AND TIME_STAMP=(SELECT (MAX(TIMESTAMP) FROM "+self.table_name+" GROUP BY USER_NAME WHERE USER_NAME='"+user_name+"')"
        print(querry)
        mycursor.execute(querry)
        result=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        la = None
        if(len(result)>0):
            la = LoginAttempt(result[0][1],result[0][2],result[0][3],result[0][4])
        return la
    
    def getAllAttemptsUser(self,user_name,epochtime=None):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        timequerry=""
        if(epochtime!=None):
            timequerry=" AND datetime(TIMESTAMP) BETWEEN "+str(epochtime)+" AND datetime('now','localtime') "
        querry="SELECT * FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"' "+timequerry 
        mycursor.execute(querry)
        result=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        la = []
        for rec in result:
            la.append(LoginAttempt(rec[1],rec[2],rec[3],rec[4]))
        return la
    
    def getAllAttemptsIp(self,ip,epochtime=None):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        timequerry=""
        if(epochtime!=None):
            timequerry=" AND datetime(TIMESTAMP) BETWEEN "+str(epochtime)+" AND datetime('now','localtime') "
        querry="SELECT * FROM "+self.table_name+" WHERE IP='"+ip+"' "+timequerry 
        mycursor.execute(querry)
        result=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        la = []
        for rec in result:
            la.append(LoginAttempt(rec[1],rec[2],rec[3],rec[4]))
        return la
    
    def getAllAttempts(self,epochtime=None):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        timequerry=""
        if(epochtime!=None):
            timequerry=" WHERE datetime(TIMESTAMP) BETWEEN datetime("+str(epochtime)+", 'unixepoch', 'localtime') AND  datetime('now','localtime') "
        querry="SELECT * FROM "+self.table_name+(timequerry if epochtime!=None else "")
        print(querry)
        mycursor.execute(querry)
        result=[]
        users=[]
        try:
            result=mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        user = None
        for rec in result:
            users.append(LoginAttempt(result[1],result[2],result[3],result[4]))
        return users
    
    def removeAttempt(self,user_name,timestamp):
        conn = sqlite3.connect(self.database)
        mycursor=conn.cursor()
        querry="DELETE FROM "+self.table_name+" WHERE USER_NAME='"+user_name+"'"
        
        try:
            mycursor.execute(querry)
            conn.commit()
            mycursor.close()
            conn.close()
            return True
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return False    
        
    def addAttempt(self,attempt):
        conn = sqlite3.connect(self.database)
        vals=[(attempt.user_name,attempt.ip,attempt.success)]
        mycursor=conn.cursor()
        sql = """INSERT INTO """+self.table_name+""" (USER_NAME,IP,SUCCESS) VALUES (?,?,?)"""
        
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
        sql+="USER_NAME VARCHAR(32) NOT NULL ,"
        sql+="IP VARCHAR(128) NOT NULL,"
        sql+="TIMESTAMP TEXT NOT NULL DEFAULT (datetime('now','localtime')) UNIQUE,"
        sql+="SUCCESS BOOLEAN NOT NULL);"
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name+" created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
        
           
if __name__ == '__main__':
    ud=User_Data("user.db","random")
    ud.create_table()
    lad=LoginAttempt_Data("loginattempt.db","random")
    lad.create_table()
    lad.addAttempt(LoginAttempt("admin","196.168.0.6",None,True))
    lad.getAllAttempts()
    #ud.addUser(User("random78","random9","random"))
    for us in ud.getAllUsers():
        print(us)
    fromtime=datetime.now()-timedelta(minutes=30)
    epochtime=time.mktime(fromtime.timetuple())    
    for la in lad.getAllAttempts(int(epochtime)):
        print(la)