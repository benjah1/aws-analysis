import peewee  
from awsanalysis.a_analyzer import AAnalyzer

class SgNotInUsed(AAnalyzer):

    def dep(self):
        return ["Ec2Loader", "SgLoader"]

    def analyze(self):
        """
        Why keeping security group that is not in used?
        Oh, unless it is used by RDS or such
        """
        db = self._dbMgr.getDB()
        query = db.execute_sql("""
SELECT 
    sg.id,
    sg.name
FROM sgtable AS sg
LEFT JOIN ec2sgtable AS ec2sg ON sg.id = ec2sg.sgid
WHERE ec2sg.id IS NULL;
        """)

        print("======")
        print("Report - Security Group Not In Used Anaylzer")
        print("======")
        print("The following security may not be in used,")
        for row in query.fetchall():
            print("  * {}: {}".format(row[0], row[1]))

        print("") 

