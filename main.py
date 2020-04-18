from services.updater import Updater

import time
import sys
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)


MYSQL_SETTINGS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "server"
}

def main():

    """ Every second the updater class is used to get changes from mysql log """

    updater = Updater()

    while True:
        time.sleep(1)
        
        stream = BinLogStreamReader(
            connection_settings=MYSQL_SETTINGS,
            server_id=100,
            only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

        for binlogevent in stream:
            prefix = {"table": binlogevent.table, "schema": binlogevent.schema}

            for row in binlogevent.rows:
                if isinstance(binlogevent, DeleteRowsEvent):
                    vals = row["values"]
                    updater.pushDelete(prefix,vals)

                elif isinstance(binlogevent, UpdateRowsEvent):
                    vals = row["after_values"]
                    updater.pushUpdate(prefix,vals)

                elif isinstance(binlogevent, WriteRowsEvent):
                    vals = row["values"]
                    updater.pushIsert(prefix,vals)

        updater.close()
        sys.stdout.flush()

main()
