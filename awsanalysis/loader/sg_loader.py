import peewee
from awsanalysis.a_loader import ALoader
import boto3

class SgLoader(ALoader):
    def dep(self):
        return set()

    def setup(self):
        db = self._dbMgr.getDB()

        class SgTable(peewee.Model):
            id = peewee.CharField(primary_key=True)
            name = peewee.CharField()

            class Meta:
                database = db

        """
        type: 1:ingres ip, 2:ingree sg, 6:egress ip, 7:egress sg
        """
        class SgRuleTable(peewee.Model):
            id = peewee.IntegerField(primary_key=True)
            sgid = peewee.CharField()
            ruleType = peewee.IntegerField()
            fromPort = peewee.CharField()
            toPort = peewee.CharField()
            source = peewee.CharField()
            protocol = peewee.CharField()

            class Meta:
                database = db

        self._dbMgr.addModel("SgTable", SgTable)
        self._dbMgr.addModel("SgRuleTable", SgRuleTable)
        SgTable.create_table()
        SgRuleTable.create_table()

    def load(self):
        filters = []
        if self._conf.get("vpcid", False):
            filters = [{
                'Name': 'vpc-id',
                'Values': [self._conf.get("vpcid")]
            }]

        ec2 = boto3.client('ec2')
        response = ec2.describe_security_groups(Filters=filters)

        sgArr = []
        sgRuleArr = []

        for sg in response["SecurityGroups"]:
           tmpSgArr, tmpSgRuleArr = self.insertSg(sg)
           sgArr = sgArr + tmpSgArr
           sgRuleArr = sgRuleArr + tmpSgRuleArr

        if (sgArr):
            self._dbMgr.getModel("SgTable").insert_many(sgArr).execute();
        if (sgRuleArr):
            self._dbMgr.getModel("SgRuleTable").insert_many(sgRuleArr).execute();

    def insertSg(self, sg):
        sgData = {
            "id": sg["GroupId"],
            "name": sg.get("GroupName", "")
        }
        sgRuleArr = []

        marked = False
        for permission in sg.get("IpPermissions", []):
            for ip in permission["IpRanges"]:
                sgRuleArr = sgRuleArr + self.insertRule(sg, 1, permission, ip)
                marked = True
            for sg in permission["UserIdGroupPairs"]:
                sgRuleArr = sgRuleArr + self.insertRule(sg, 2, permission, sg)
                marked = True
        for permission in sg.get("IpPermissionsEgress", []):
            for ip in permission["IpRanges"]:
                sgRuleArr = sgRuleArr + self.insertRule(sg, 6, permission, ip)
                marked = True
            for sg in permission["UserIdGroupPairs"]:
                sgRuleArr = sgRuleArr + self.insertRule(sg, 7, permission, sg)
                marked = True

        if not marked :
            sgRuleArr = sgRuleArr + self.insertRule(sg, 11, {}, sg)

        return [sgData], sgRuleArr

    def insertRule(self, sg, ruleType, permission, rule):
        source = ""
        if ruleType == 1 or ruleType == 6 :
            source = rule.get("CidrIp", "")
        elif ruleType == 2 or ruleType == 7 :
            source = rule.get("GroupId", "")
        elif ruleType == 11 :
            source = str(rule) # unknown data type?

        sgRuleData = {
            "sgid": sg["GroupId"],
            "ruleType": ruleType,
            "fromPort": permission.get("FromPort", "??"),
            "toPort": permission.get("ToPort", "??"),
            "source": source,
            "protocol": permission.get("IpProtocol", "??")
        }

        return [sgRuleData]

