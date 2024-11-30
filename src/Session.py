# from pymongogettersetter import MongoGetterSetter
from src.Database import Database   
from uuid import uuid4
from time import time

db = Database.get_connection()

# class SessionCollection(metaclass=MongoGetterSetter):
#     def __init__(self,id):
#         self._collections = db.sessions
#         self._filter_query = {"id": id }

class Session:
    def __init__(self,id):
        self.id = id
        # self.collection = SessionCollection(id)
        
    @staticmethod
    def register_session(username,validity =604800,_type = 'plain'):
        uuid = str(uuid4())
        collection = db.sessions
        """
        if users logsout, we set active to false and delete the session
        if users logs in, we set active to true and create the new session
        if user inactive for 7 days, we discard the session and discard active = True since validity expired
        
        types :
        1. plain - username and password for authentication
        2. api - API Key user for authentication
        """
        collection.insert_one(
            {
                'id' : uuid,
                'username' : username,
                'time' : time(),
                'validity' : validity, #7days 
                'active' : True,
                'type' : _type
            }
        )
        return Session(uuid)