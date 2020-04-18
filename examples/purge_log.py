import os
import sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
# all things above is to allow python import classes out of test folder

from services.dbconn import DBConn
from services.elastic_updater_adapter import ElasticAdapter
from services.elastic import Elastic

dbconn = DBConn(_host='127.0.0.1', _port=3306, _user='root', _passwd='server', _db='your_database')

res = dbconn.purgeLogFiles()

print(res)