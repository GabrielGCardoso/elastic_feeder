import sys
import re
import pathlib
from services.dbconn import DBConn

## get name from args to create model from database table
if len(sys.argv) >= 2 :
    model = sys.argv[1]
else:
    model = "client"

dbconn = DBConn(_host='127.0.0.1', _port=3306, _user='user', _passwd='password', _db='your_database')

descriptions, _ = dbconn.execGetAll("SELECT * FROM `%s` ORDER BY `id` DESC " % model)

dbconn.closeConn()

## writing the constructor from the class
class2write = """
from services.dbconn import DBConn

class %s():
    obj = []

    def __init__(self,obj):
        self.obj = {
""" % model

fks = []
dates = []
times = []
for desc in descriptions:

    class2write += "            " 

    if(re.search("_id",desc[0])):
        _fk = desc[0].replace('_id','')
        fks.append(_fk) 
        class2write += "'%s' : obj['%s'] if '%s' in obj else None, " % (_fk, desc[0], desc[0])

    elif(re.search("id_",desc[0])):
        _fk = desc[0].replace('id_','')
        fks.append(_fk)
        class2write += "'%s' : obj['%s'] if '%s' in obj else None, " % (_fk, desc[0], desc[0])

    else:
        class2write += "'%s' : obj['%s'] if '%s' in obj else None, " % (desc[0], desc[0], desc[0])

    class2write += "\n"

    if(re.search("date",desc[0])):
        dates.append(desc[0])

    if(re.search("time",desc[0])):
        times.append(desc[0])

class2write += "        "
class2write += "}" 
class2write +="\n\n"

## writing functions to get foreign tables
for fk in fks:
    class2write += "    "
    class2write += "def get_%s(self, id):\n" % fk
    class2write += "        "
    class2write += "return self.db.find2Obj(' SELECT * FROM %s WHERE id=%%s ' %% (id) )\n\n" % fk

## writing function to start all fuctions to get fk tables
class2write += """
    def getFks(self):
        self.db = DBConn()\n"""
for fk in fks:   
    class2write += "        " 
    class2write += "self.obj['%s'] = None if self.obj['%s'] == None or len(str((self.obj['%s']))) == 0 else self.get_%s(self.obj['%s']) " % (fk, fk, fk, fk, fk)
    class2write += "\n"
class2write += "        "
class2write += "self.db.closeConn()\n"

if(len(dates)>0):
    class2write += """
    def dateTreatment(self,obj):
        # treatment of time objects 
        return None if obj == '0000-00-00' else obj
        """

if(len(times)>0):
    class2write += """
    def timeTreatment(self,obj):
        # treatment of time objects 
        return None if obj == None else str(obj)
        """
        
## writing the function to return the object from this model
class2write += """
    def getObj(self):
        # treatment of data objects \n"""
for date in dates:   
    class2write += "        " 
    class2write += "self.obj['%s'] = self.dateTreatment(self.obj['%s']) " % (date, date)
    class2write += "\n"

class2write += "        # treatment of time objects\n" 

for time in times:   
    class2write += "        " 
    class2write += "self.obj['%s'] = self.timeTreatment(self.obj['%s']) " % (time, time)
    class2write += "\n"

class2write += "        return self.obj" 

path  = str(pathlib.Path(__file__).parent.absolute())
path += "/models/"+model+"_model.py" 

f = open(path, "w")
f.write(class2write)
f.close()
