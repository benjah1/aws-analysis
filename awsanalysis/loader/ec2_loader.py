import peewee
from awsanalysis.a_loader import ALoader
import boto3
import logging

class Ec2Loader(ALoader):
    def dep(self):
        return ["TagLoader"]

    def setup(self):
        db = self._dbMgr.getDB()

        class Ec2Table(peewee.Model):
            id = peewee.CharField(primary_key=True)
            name = peewee.CharField()
            amiId = peewee.CharField()
            instanceType = peewee.CharField()
            privateIpAddress = peewee.CharField()
            subnetId = peewee.CharField()
            vpcId = peewee.CharField()
            architecture = peewee.CharField()
            ebsOptimized = peewee.BooleanField()
            hypervisor = peewee.CharField()
            virtualizationType = peewee.CharField()

            class Meta:
                database = db

        class Ec2VolTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            ec2Id = peewee.CharField()
            volId = peewee.CharField()
            deviceName = peewee.CharField()

            class Meta:
                database = db

        class Ec2EniTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            ec2Id = peewee.CharField()
            attachmentId = peewee.CharField()
            eniId = peewee.CharField()

            class Meta:
                database = db

        class Ec2SgTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            ec2Id = peewee.CharField()
            sgId = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("Ec2Table", Ec2Table)
        self._dbMgr.addModel("Ec2VolTable", Ec2VolTable)
        self._dbMgr.addModel("Ec2EniTable", Ec2EniTable)
        self._dbMgr.addModel("Ec2SgTable", Ec2SgTable)
        Ec2Table.create_table()
        Ec2VolTable.create_table()
        Ec2EniTable.create_table()
        Ec2SgTable.create_table()

    def load(self):
        filters = []
        if self._conf.get("vpcid", False):
            filters = [{
                'Name': 'vpc-id',
                'Values': [self._conf.get("vpcid")]
            }]

        ec2 = boto3.client('ec2')
        response = ec2.describe_instances(Filters=filters)

        ec2Arr = []
        tagArr = []
        ec2VolArr = []
        ec2EniArr = []
        ec2SgArr = []

        for r in response["Reservations"]:
            for i in r["Instances"]:
               tmpEc2Arr, tmpTagArr, tmpEc2VolArr, tmpEc2EniArr, tmpEc2SgArr  = self.insertEc2(i)
               ec2Arr = ec2Arr + tmpEc2Arr
               tagArr = tagArr + tmpTagArr
               ec2VolArr = ec2VolArr + tmpEc2VolArr
               ec2EniArr = ec2EniArr + tmpEc2EniArr
               ec2SgArr = ec2SgArr + tmpEc2SgArr

        if (ec2Arr):
            self._dbMgr.getModel("Ec2Table").insert_many(ec2Arr).execute()
        if (tagArr):
            self._dbMgr.getModel("TagTable").insert_many(tagArr).execute()
        if (ec2VolArr):
            self._dbMgr.getModel("Ec2VolTable").insert_many(ec2VolArr).execute()
        if (ec2EniArr):
            self._dbMgr.getModel("Ec2EniTable").insert_many(ec2EniArr).execute()
        if (ec2SgArr):
            self._dbMgr.getModel("Ec2SgTable").insert_many(ec2SgArr).execute()

    def insertEc2(self, ec2):
        name = ""
        for tag in ec2.get("Tags", []):
            if tag.get('Key', "") == 'Name':
                name = tag.get('Value', "")

        ec2Data = {
            "id": ec2["InstanceId"],
            "name": name,
            "amiId": ec2["ImageId"],
            "instanceType": ec2["InstanceType"],
            "privateIpAddress": ec2["PrivateIpAddress"],
            "subnetId": ec2["SubnetId"],
            "vpcId": ec2["VpcId"],
            "architecture": ec2["Architecture"],
            "ebsOptimized": ec2["EbsOptimized"],
            "hypervisor": ec2["Hypervisor"],
            "virtualizationType": ec2["VirtualizationType"]
        }

        tagArr = []
        ec2VolArr = []
        ec2EniArr = []
        ec2SgArr = []

        for tag in ec2.get("Tags", []):
            tagData = {
                "resId": ec2["InstanceId"],
                "loader": "Ec2Loader",
                "key": tag["Key"],
                "value": tag["Value"]
            }
            tagArr = tagArr + [tagData]

        for ebs in ec2.get("BlockDeviceMappings", []):
            # not sure how the handler nfs yet, since I dont have data
            if (ebs["Ebs"]):
                ec2VolData = {
                    "ec2Id": ec2["InstanceId"],
                    "volId": ebs["Ebs"]["VolumeId"],
                    "deviceName": ebs["DeviceName"]
                }
                ec2VolArr = ec2VolArr + [ec2VolData]

        for eni in ec2.get("NetworkInterfaces", []):
            ec2EniData = {
                "ec2Id": ec2["InstanceId"],
                "attachmentId": eni["Attachment"]["AttachmentId"],
                "eniId": eni["NetworkInterfaceId"]
            }
            ec2EniArr = ec2EniArr + [ec2EniData]

        for sg in ec2.get("SecurityGroups", []):
            ec2SgData = {
                "ec2Id": ec2["InstanceId"],
                "sgId": sg["GroupId"]
            }
            ec2SgArr = ec2SgArr + [ec2SgData]

        return [ec2Data], tagArr, ec2VolArr, ec2EniArr, ec2SgArr

