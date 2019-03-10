import peewee  
from awsanalysis.a_loader import ALoader
import boto3

class Ec2Loader(ALoader):
    def dep(self):
        return []

    def setup(self):
        db = self._dbMgr.getDB()

        class Ec2Table(peewee.Model):
            id = peewee.CharField(primary_key=True)
            name = peewee.CharField()

            class Meta:
                database = db

        class Ec2SgTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            ec2id = peewee.CharField()
            sgid = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("Ec2Table", Ec2Table)
        self._dbMgr.addModel("Ec2SgTable", Ec2SgTable)
        Ec2Table.create_table()
        Ec2SgTable.create_table()
 
    def load(self):
        """ todo: use insert_many for performance """
        filters = []
        if self._conf.get("vpcid", False): 
            filters = [{
                'Name': 'vpc-id',
                'Values': [self._conf.get("vpcid")]
            }]

        ec2 = boto3.client('ec2')
        response = ec2.describe_instances(Filters=filters)

        ec2Arr = []
        ec2sgArr = []

        for r in response["Reservations"]:
            for i in r["Instances"]:
               tmpEc2Arr, tmpEc2sgArr = self.insertEc2(i)
               ec2Arr = ec2Arr + tmpEc2Arr 
               ec2sgArr = ec2sgArr + tmpEc2sgArr

        self._dbMgr.getModel("Ec2Table").insert_many(ec2Arr).execute()
        self._dbMgr.getModel("Ec2SgTable").insert_many(ec2sgArr).execute()

    def insertEc2(self, ec2):
        name = ""
        for tag in ec2.get("Tags", []):
            if tag.get('Key', "") == 'Name':
                name = tag.get('Value', "")
        
        ec2Data = {
            "id": ec2["InstanceId"], 
            "name": name
        }

        ec2sgArr = []

        for sg in ec2["SecurityGroups"]:
            ec2sgData = {
                "ec2id": ec2["InstanceId"], 
                "sgid": sg["GroupId"]
            }
            ec2sgArr = ec2sgArr + [ec2sgData]

        return [ec2Data], ec2sgArr
