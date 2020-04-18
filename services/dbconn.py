import pymysql
import json

import os
import sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

class DBConn():
    conn    = None
    cur     = None

    _host = _port = _user = _passwd = _db = None


    def refreshConn(self):
        self.conn = pymysql.connect(host=self._host,
                                    port=self._port,
                                    user=self._user,
                                    passwd=self._passwd,
                                    db=self._db)
        self.cur = self.conn.cursor()

    def _getDefaulConfig(self):
        with open('config.json') as json_file:
            return json.load(json_file)["database"]

    def __init__(self,
                 _host  = None, 
                 _port  = None, 
                 _user  = None, 
                 _passwd= None, 
                 _db    = None):
        
        if(_host == None or _port == None or _user == None or _passwd == None or _db == None):

            obj_cfg = self._getDefaulConfig()
            self._host  = obj_cfg["host"]
            self._port  = obj_cfg["port"]
            self._user  = obj_cfg["user"]
            self._passwd= obj_cfg["passwd"]
            self._db    = obj_cfg["db"]
        
        self.refreshConn()        

    def closeConn(self):
        self.cur.close()
        self.conn.close()

    def find2Obj (self, _sqlQuery):        
        descritpions, value = self.find(_sqlQuery)
        obj = {}
        i = 0

        if(descritpions == None or value == None):
            return None

        else:
            for desc in descritpions:
                obj[desc[0]] = None if(len (str(value[i])) < 1) else value[i]
                i+=1
            return obj

    def find(self, _sqlQuery):
        """ Execute an sql command and returns the result """
        try:
            self.cur.execute(_sqlQuery)
            return self.cur.description, self.cur.fetchone()
        except Exception as e:
            print(e)
            return None, None

    def execGetAll(self, _sqlQuery):
        """ Execute an sql for getAll rows and returns the result """
        try:
            self.cur.execute(_sqlQuery)
            description  = self.cur.description
            
            return self.cur.description, self.cur
            
        except Exception as e:
            print(e)
            return None, None

    def purgeLogFiles(self):
        """ Execute an sql command to purge all binary logs before now """
        try:
            # self.cur.execute("PURGE BINARY LOGS BEFORE NOW()")
            self.cur.execute("PURGE BINARY LOGS BEFORE DATE(NOW() - INTERVAL 1 DAY) + INTERVAL 0 SECOND")
        except Exception as e:
            print(e)
        finally:
            self.closeConn()
