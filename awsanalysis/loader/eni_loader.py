import peewee
from awsanalysis.a_loader import ALoader
import boto3
import logging

class EniLoader(ALoader):
    def dep(self):
        return {"TagLoader"}

    def setup(self):
        db = self._dbMgr.getDB()

        class EniTable(peewee.Model):
            id = peewee.CharField(primary_key=True)
            attachId = peewee.CharField(null=True)
            az = peewee.CharField()
            interfaceType = peewee.CharField()
            requesterId = peewee.CharField(null=True)
            status = peewee.CharField()
            subnetId = peewee.CharField()
            vpcId = peewee.CharField()
            privateIpAddress = peewee.CharField()

            class Meta:
                database = db

        class EniAttachTable(peewee.Model):
            id = peewee.CharField(primary_key=True)
            resId = peewee.CharField(null=True)
            instanceOwnerId = peewee.CharField()
            status = peewee.CharField()

            class Meta:
                database = db

        class EniSgTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            eniId = peewee.CharField()
            sgId = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("EniTable", EniTable)
        self._dbMgr.addModel("EniAttachTable", EniAttachTable)
        self._dbMgr.addModel("EniSgTable", EniSgTable)
        EniTable.create_table()
        EniAttachTable.create_table()
        EniSgTable.create_table()

    def load(self):
        filters = []
        if self._conf.get("vpcid", False):
            filters = [{
                'Name': 'vpc-id',
                'Values': [self._conf.get("vpcid")]
            }]

        ec2 = boto3.client('ec2')
        response = ec2.describe_network_interfaces(Filters=filters)

        eniArr = []
        tagArr = []
        eniAttachArr = []
        eniSgArr = []

        for e in response["NetworkInterfaces"]:
            tmpEniArr, tmpTagArr, tmpEniAttachArr, tmpEniSgArr = self.insertEni(e)
            eniArr = eniArr + tmpEniArr
            tagArr = tagArr + tmpTagArr
            eniAttachArr = eniAttachArr + tmpEniAttachArr
            eniSgArr  = eniSgArr  + tmpEniSgArr

        if (eniArr):
            self._dbMgr.getModel("EniTable").insert_many(eniArr).execute()
        if (tagArr):
            self._dbMgr.getModel("TagTable").insert_many(tagArr).execute()
        if (eniAttachArr):
            self._dbMgr.getModel("EniAttachTable").insert_many(eniAttachArr).execute()
        if (eniSgArr):
            self._dbMgr.getModel("EniSgTable").insert_many(eniSgArr).execute()

    def insertEni(self, eni):
        eniData = {
            "id": eni["NetworkInterfaceId"],
            "attachId": eni.get("Attachment", {}).get("AttachmentId", None),
            "az": eni["AvailabilityZone"],
            "interfaceType": eni["InterfaceType"],
            "requesterId": eni.get("RequesterId", None),
            "status": eni["Status"],
            "subnetId": eni["SubnetId"],
            "vpcId": eni["VpcId"],
            "privateIpAddress": eni.get("privateIpAddress", "")
        }

        eniAttachArr = []
        if (eni.get("Attachment", None)):
            a = eni["Attachment"]
            eniAttachData = {
                "id": a["AttachmentId"],
                "resId": a.get("InstanceId", None),
                "instanceOwnerId": a["InstanceOwnerId"],
                "status": a["Status"]
            }
            eniAttachArr = eniAttachArr + [eniAttachData]

        eniSgArr = []
        tagArr = []

        for sg in eni.get("Groups", []):
            eniSgData = {
                "eniId": eni["NetworkInterfaceId"],
                "sgId": sg["GroupId"]
            }
            eniSgArr = eniSgArr + [eniSgData]

        for tag in eni.get("TagSet", []):
            tagData = {
                "resId": eni["NetworkInterfaceId"],
                "loader": "EniLoader",
                "key": tag["Key"],
                "value": tag["Value"]
            }
            tagArr = tagArr + [tagData]

        return [eniData], tagArr, eniAttachArr, eniSgArr

