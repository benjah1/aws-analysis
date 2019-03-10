import peewee  
from awsanalysis.a_analyzer import AAnalyzer

class SgWideOpen(AAnalyzer):

    def dep(self):
        return ["Ec2Loader", "SgLoader"]

    def analyze(self):
        """
        0.0.0.0 and 10.0.0.0 should not be open without aware
        """
        db = self._dbMgr.getDB()
        query = db.execute_sql("""
SELECT 
    sg.id, 
    sg.name,
    sgr.source,
    sgr.protocol,
    sgr.fromPort,
    sgr.toPort 
FROM sgruletable AS sgr
LEFT JOIN sgtable AS sg ON sgr.sgid = sg.id
WHERE sgr.ruletype in (1) 
    AND (sgr.source LIKE '0.0.0.0%' OR sgr.source LIKE '10.0.0.0%')
ORDER BY sg.id, sgr.protocol, sgr.source, sgr.fromPort;
        """)

        print("======")
        print("Report - Security Group Wide Open Anaylzer")
        print("======")
        print("The following security may be opening too much,")

        sgid = ""
        source = ""
        protocol = ""
        fromPort = ""
        for row in query.fetchall():
            if sgid != row[0] :
                print("  * {}: {}".format(row[0], row[1]))
                sgid = row[0]
                source = ""
                protocol = ""
                fromPort = ""

            if source != row[2] :
                print("    From {}".format(row[2]))
                source = row[2]
                protocol = ""
                fromPort = ""

            print("      {} {}".format(row[3], row[4]))

        print("") 

