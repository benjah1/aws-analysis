from peewee import SqliteDatabase
import os.path
import datetime

class CDBMgr:
    def __init__(self, conf):
        print("-> DBMgr init")
        self._conf = conf
        dbFile = self.getDBFile()
        self._db = SqliteDatabase(dbFile)
        self._model = {}

    def getDBFile(self):
        dbFile = self._conf.get("sqliteDB", "data.db")
        if self._conf.get('load', True):
            if os.path.isfile(dbFile):
                timeStamp =  datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                os.rename(dbFile, "{}_{}.db".format(dbFile.split(".")[0], timeStamp))
        return dbFile

    def getDB(self):
        return self._db

    def getModel(self, key):
        return self._model.get(key)

    def addModel(self, key, model):
        self._model[key] = model
