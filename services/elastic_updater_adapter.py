
class ElasticAdapter():
    default_type    = None
    default_index   = None

    def __init__(self, _index, _type):
        self.default_type  = _type
        self.default_index = _index

    def setDefaultIndex(self, _index):
        """ set the default index """
        self.default_index = _index

    def setDefaultType(self, _type):
        """ set the default type """
        self.default_type = _type

    def getDefaultIndex(self):
        """ returns variable default_index """
        return self.default_index

    def getDefaultType(self):
        """ returns variable default_type """
        return self.default_type

    def adaptObj(self, _obj, _type=None, _index=None):
        """ transforms an object to elastic object to insert """
        _index  = self.default_index if (_index == None) else _index
        _type   = self.default_type  if (_type  == None) else _type

        return ({
            "_id"   : _obj['id'],
            "_index": _index,
            "_type" : _type,
            "_source"   : _obj
        })

    def adaptArrayObjects(self,_input_arr,_type=None, _index=None):
        """ transforms an array of objects to elastic array of objects """

        _index  = self.default_index if (_index == None) else _index
        _type   = self.default_type  if (_type  == None) else _type

        _return_arr = []

        for _row in _input_arr:
            _return_arr.append(self.adaptObj(_row,_type, _index))

        return _return_arr
        