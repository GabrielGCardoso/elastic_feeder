
from datetime import datetime
from elasticsearch import Elasticsearch, helpers


class Elastic():

    es_client = None

    def __init__(self):
        self.es_client = Elasticsearch()

    def removeIndex(self, _index):
        """ this function remove the index """
        return self.es_client.indices.delete(_index)

    def resetIndex(self, _index):
        """ this function remove and create the index """
        if(es_client.indices.exists(_index)):
            self.removeIndex(_index)

        return self.es_client.indices.create(_index)

    def findById(self, _index, _id):
        """ this function can get a row from elastic """
        return self.es_client.get(index=_index, id=_id)['_source']

    def push(self, _adapted_obj):
        """ this function can insert or update in elastic """
        return self.es_client.index(index=_adapted_obj["_index"], id=_adapted_obj["_id"], body=_adapted_obj["_source"])['result']
        
    def delete(self, _adapted_obj):
        """ this function delete a row from elastic """
        return self.es_client.delete(index=_adapted_obj["_index"], id=_adapted_obj["_id"])

    def bulkInsert(self, _adapted_obj_array):
        """ this function is used to insert or update a package of rows from adapt class """

        return helpers.bulk(self.es_client, _adapted_obj_array)   