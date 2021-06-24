'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,user_name,password,mail):
        self.user_name=user_name
        self.password=password
        self.mail=mail
        
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
    
class User_Data:
    
    def __init__(self,database,logger_name):
        self.database=database
        self.logger_name=logger_name
        self.table_name="User"
        self.create_table()
    
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
            
if __name__ == '__main__':
    ud=User_Data("user.db","random")
    ud.create_table()
    ud.addUser(User("random78","random9","random"))
    for us in ud.getAllUsers():
        print(us)