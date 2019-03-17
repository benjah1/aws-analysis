import peewee  
from awsanalysis.a_loader import ALoader

class TagLoader(ALoader):
    def dep(self):
        return []

    def setup(self):
        db = self._dbMgr.getDB()

        class TagTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            resId = peewee.CharField()
            loader = peewee.CharField()
            key = peewee.CharField()
            value = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("TagTable", TagTable)
        TagTable.create_table()
 
    def load(self):
        return

