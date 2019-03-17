import peewee  
from awsanalysis.a_loader import ALoader

class TestLoader(ALoader):
    def dep(self):
        return []

    def setup(self):
        print("-> -> TestLoader setup db")
        print(self._conf)
        
        db = self._dbMgr.getDB()

        class TestTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            name = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("TestTable", TestTable)
        TestTable.create_table()

    def load(self):
        print("-> -> TestLoader load")
        self._dbMgr.getModel("TestTable").insert_many([
                {"name": "a"},
                {"name": "b"}
            ]).execute()

