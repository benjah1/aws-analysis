import peewee
from awsanalysis.a_loader import ALoader
import boto3
import datetime
import logging

class LogsLoader(ALoader):
    def dep(self):
        return set()

    def setup(self):
        db = self._dbMgr.getDB()

        class LogsTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            eventId = peewee.CharField()
            groupName = peewee.CharField()
            streamName = peewee.CharField()
            ingestionTime = peewee.IntegerField()
            timestamp = peewee.IntegerField()
            message = peewee.CharField()
            
            class Meta:
                database = db

        self._dbMgr.addModel("LogsTable", LogsTable)
        LogsTable.create_table()
 
    def load(self):
        return
        groups = self._conf.get("groups", [])
        now = int(datetime.datetime.now().timestamp() * 1000)
        self._st = self._conf.get("start_time", now - 60 * 2 * 1000)
        self._et = self._conf.get("end_time", now)
        eventArr = []

        print("{} {}".format(self._st, self._et))
        LogsTable = self._dbMgr.getModel("LogsTable")

        for group in groups:
            for events in self.get_logs(group):
                eventArr = eventArr + self.insert_events(group, events)
                while len(eventArr) > 900:
                    current = eventArr[:900]
                    LogsTable.insert_many(current).execute()
                    eventArr = eventArr[900:]
        
        if (len(eventArr) > 0):
            LogsTable.insert_many(eventArr).execute()

    def get_logs(self, group):
        kwargs = {
            "logGroupName": group, 
            "startTime": self._st,
            "endTime": self._et
        }

        paginator = boto3.client('logs').get_paginator('filter_log_events')
        for page in paginator.paginate(**kwargs):
            print("status: {}".format(page.get('searchedLogStreams')))
            print("num of event: {}".format(len(page.get('events', []))))
            yield page.get('events', [])

    def insert_events(self, group, events):
        eventArr = []
        for e in events:
            eventArr = eventArr + [{
                "groupName": group,
                "eventId": e["eventId"],
                "streamName": e["logStreamName"],
                "ingestionTime": e["ingestionTime"],
                "timestamp": e["timestamp"],
                "message": e["message"]
            }]
        return eventArr

