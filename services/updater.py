from .elastic import Elastic
from .elastic_updater_adapter import ElasticAdapter
from .factory_model import FactoryModel

class Updater():
    MaxDeletes  = None
    MaxUpdates  = None
    MaxInserts  = None

    deleteds    = None
    updateds    = None
    inserteds   = None

    es = None
    adapter = None

    def __init__(self):
        self.MaxDeletes = 0
        self.MaxUpdates = 0
        self.MaxInserts = 0

        self.deleteds   = []
        self.updateds   = []
        self.inserteds  = []
        
        self.es = Elastic()
        self.adapter = ElasticAdapter("client","document")
    
    def _verifyAndPushObj(self,obj,prefix):
        obj, index = FactoryModel(prefix, obj, get_from_db=True).getObj() 
        if(obj != None):
            self.adapter.setDefaultIndex(index)
            adapted_obj = self.adapter.adaptObj(obj)
            print("pushed")
            print(adapted_obj["_id"],index)
            self.es.push(_adapted_obj = adapted_obj)
    
    def _verifyAndDeleteObj(self,obj,prefix):
        obj, index = FactoryModel(prefix, obj).getObj()
        if(index != None):
            self.adapter.setDefaultIndex(index)
            adapted_obj = self.adapter.adaptObj(obj)
            print("deleted")
            print(adapted_obj["_id"],index)
            self.es.delete(_adapted_obj=adapted_obj)

    def pushDelete(self, prefix, obj):        
        self.deleteds.append(obj)
        if(len(self.deleteds) > self.MaxDeletes):
            self._verifyAndDeleteObj(obj,prefix)

    def pushUpdate(self, prefix, obj):
        self.updateds.append(obj)
        if(len(self.updateds) > self.MaxUpdates):
            self._verifyAndPushObj(obj,prefix)                

    def pushIsert(self, prefix, obj):
        self.inserteds.append(obj)
        if(len(self.inserteds) > self.MaxInserts):
            self._verifyAndPushObj(obj,prefix)

    def close(self):
        self.MaxDeletes = len(self.deleteds)
        self.MaxUpdates = len(self.updateds)
        self.MaxInserts = len(self.inserteds)

        self.deleteds  = []
        self.updateds  = []
        self.inserteds = []

