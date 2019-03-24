import peewee
from awsanalysis.a_loader import ALoader
import boto3
import logging

class LogsFlowLogsLoader(ALoader):
    def dep(self):
        return {"LogsLoader"}

    def setup(self):
        db = self._dbMgr.getDB()

        class LogsFlowLogsTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            eventId = peewee.CharField()
            version = peewee.IntegerField()
            accountId = peewee.IntegerField()
            interfaceId = peewee.CharField()
            srcaddr = peewee.CharField()
            dstaddr = peewee.CharField()
            srcport = peewee.IntegerField()
            dstport = peewee.IntegerField()
            protocol = peewee.IntegerField()
            packets = peewee.IntegerField()
            bytes = peewee.IntegerField()
            start = peewee.IntegerField()
            end = peewee.IntegerField()
            action = peewee.CharField()
            status = peewee.CharField()
            
            class Meta:
                database = db

        self._dbMgr.addModel("LogsFlowLogsTable", LogsFlowLogsTable)
        LogsFlowLogsTable.create_table()
 
    def load(self):
        logsArr = []
        LogsFlowLogsTable = self._dbMgr.getModel("LogsFlowLogsTable")
        for log in self.get_logs():
            tmpArr = self.insert_log(log)
            logsArr = logsArr + tmpArr
            
            while len(logsArr) > 900:
                current = logsArr[:900]
                print("insert {} record".format(len(current)))
                LogsFlowLogsTable.insert_many(current).execute()
                logsArr = logsArr[900:]

        if (len(logsArr) > 0):
            LogsFlowLogsTable.insert_many(logsArr).execute()

    def get_logs(self):
        groups = self._conf.get("groups", [])
        LogsTable = self._dbMgr.getModel("LogsTable")

        i = 1
        notEmpty = True
        while notEmpty:
            query = LogsTable.select(
                LogsTable.eventId, 
                LogsTable.message
            ).where(LogsTable.groupName.in_(groups)).paginate(i, 10000)
            
            print(query.sql())
            rows = []
            for row in query:
                rows = rows + [row]
            
            i = i + 1
            if len(rows) > 0:
                yield rows
            else:
                notEmpty = False

    def insert_log(self, logs):
        arr = []

        for log in logs:
            message = log.message.replace('- ', '0 ')
            message = message.split(" ")

            if message[1] == 'unknown':
                print("drop {}", message)
                continue

            # print(message)
            data = {
                "eventId"   : log.eventId,
                "version"   : message[0],
                "accountId" : message[1],
                "interfaceId"   : message[2],
                "srcaddr"   : message[3],
                "dstaddr"   : message[4],
                "srcport"   : message[5],
                "dstport"   : message[6],
                "protocol"  : message[7],
                "packets"   : message[8],
                "bytes"     : message[9],
                "start"     : message[10],
                "end"       : message[11],
                "action"    : message[12],
                "status"    : message[13]
            }

            arr = arr + [data]

        return arr

