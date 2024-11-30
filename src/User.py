import pymongo 
from src.Database import Database
from time import time
from random import randint
import bcrypt
from src.Session import Session
db = Database.get_connection()
users = db.users
class User:
    def __init__(self,id):
        print("Init User with {}".format(id))
        
    @staticmethod   
    def login(username,password):
        result = users.find_one({
            "username":username
        }) 
        if result: 
            # if result['password'] == password:
            #     return True
            # else:
            #     raise Exception("Incorrect Password")
            hashpw = result['password']
            if bcrypt.checkpw(password.encode(),hashpw):
                sess = Session.register_session(username)
                return sess.id
        else:
            raise Exception("Incorrect Credentials")
    @staticmethod
    def register(username,password,confirm_password):
        if(password!=confirm_password):
            raise Exception("Password and Confirm Password do not match")
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(),salt)
        
        id = users.insert_one({
            "username":username,
            "password":password,
            "register_time":time(),
            "active":False,
            "activate_token":randint(100000,999999)
        })
        
        return id
        
    
    