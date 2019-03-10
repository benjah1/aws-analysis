import peewee  
from awsanalysis.a_analyzer import AAnalyzer

class TestAnalyzer(AAnalyzer):

    def dep(self):
        return ["TestLoader"]

    def analyze(self):
        TestTable = self._dbMgr.getModel("TestTable")
        query = TestTable.select().order_by(TestTable.name)
        for row in query:
            print(row.name)

