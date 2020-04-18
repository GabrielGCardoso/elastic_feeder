
from services.dbconn import DBConn

class clients():
    obj = []

    def __init__(self,obj):
        self.obj = {
            'id' : obj['id'] if 'id' in obj else None, 
            'name' : obj['name'] if 'name' in obj else None, 
        }

    def getObj(self):
        return self.obj