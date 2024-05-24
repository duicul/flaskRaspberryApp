import sys
import hashlib
#import sha3
from hashlib import sha3_512
from user_class import User_Data,User
import base64
class Authorization:
    
    def __init__(self):
        self.user_data = User_Data("db/user.db",'werkzeug')
        self.user_data.create_table()
        if(len(self.user_data.getAllUsers())==0):
            self.createDefaultUser()
    
    def loginUser(self,user_name,password,ip,epochtime):
        hash_sha3_512 = hashlib.sha3_512() 
        hash_sha3_512.update(password.encode()) 
        #hashlib.new("sha3_512", password.encode())
        user= self.user_data.loginUser(user_name,hash_sha3_512.hexdigest(),ip,epochtime)
        return user
    
    def registerUser(self,user_name,password,mail):
        hash_sha3_512 = hashlib.sha3_512() 
        hash_sha3_512.update(password.encode()) 
        #hash_sha3_512 = hashlib.new("sha3_512", password.encode())
        return self.user_data.addUser(User(user_name,hash_sha3_512.hexdigest(),mail))
    
    def removeUser(self,user_name): 
        return self.user_data.removeUser(user_name)
    
    def createDefaultUser(self):
        self.registerUser("admin", "admin", "admin")
    
if __name__ == '__main__':
    aut = Authorization()
    #aut.createDefaultUser()
    aut.registerUser("duicul", "pass", "Gogu")
    #print(aut.loginUser("duicul", "pass"))
    aut.removeUser("duicul")
    #print(aut.loginUser("duicul", "pass"))
    
