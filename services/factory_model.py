from models.orders_model import orders
from models.clients_model import clients
from models.items_model import items
from models.transactions_model import transactions
from models.order_logistics_model import order_logistics
from services.dbconn import DBConn

class FactoryModel():
    obj = None
    index = None

    def __init__(self, prefixs, data, get_from_db = False):
        db = DBConn()
        return self.createModel(prefixs, data)

    def createModel(self, prefixs, data, get_from_db = False):
        
        if(prefixs["schema"] == "your_table"):
            if(prefixs["table"] == "clients"):
                self.index = "clients"
                local_data = self.getDataFromDB(data) if get_from_db == True else data
                self.obj = clients(data)

            # # use the model_creater.py to create the class from database            
            # # here you'll replicate the code to others tables
            # elif(prefixs["table"] == "other_table"):   
            #     self.index = "other_table"
            #     local_data = self.getDataFromDB(data) if get_from_db == True else data
            #     self.obj = other_table(data)

        else:
            return None

    def getDataFromDB(self, data):
        return self.db.find2Obj(" SELECT * FROM %s WHERE id=%s " % (self.index, data["id"]) )

    def getObj(self):
        self.obj.getFks()
        return self.obj.getObj(), self.index