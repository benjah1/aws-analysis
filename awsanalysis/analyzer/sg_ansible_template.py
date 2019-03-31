import peewee
from awsanalysis.a_analyzer import AAnalyzer
import os

class SgAnsibleTemplate(AAnalyzer):
    def dep(self):
        return {"SgLoader"}

    def analyze(self):
        """
        Convert SG back to Ansible playbook...
        """

        db = self._dbMgr.getDB()
        query = db.execute_sql("""
SELECT 
    sg.name, 
    sgr.protocol,
    sgr.fromport, 
    sgr.toport, 
    sgr.ruletype, 
    sgr.source, 
    usg.name 
FROM sgtable AS sg
LEFT JOIN sgruletable AS sgr ON sgr.sgid = sg.id
LEFT JOIN sgtable AS usg ON sgr.source = usg.id
WHERE sgr.ruletype IN (1, 2)
group by 
    sg.name, 
    sgr.protocol,
    sgr.fromport, 
    sgr.toport, 
    sgr.ruletype, 
    sgr.source
ORDER BY sg.id, sgr.protocol, sgr.fromport, sgr.ruletype;
        """)

        sg = ''
        protocol = ''
        fromPort = ''
        toPort = ''
        stype = ''
 
        directory = "outputs/sg_ansible_template"
        if not os.path.exists(directory):
            os.makedirs(directory)      

        for row in query:
            # print(row)
            if sg != row[0]:
                sg = row[0]
                protocol = ''
                fromPort = ''
                stype = ''
                with open("{0}/{1}.yml".format(directory, sg), "w") as f:
                    f.write("""\
- name: {0} ec2 group
  ec2_group:
    name: {0}
    description: {0} EC2 group
    purge_rules: true
    vpc_id: {1}
    region: {2}
    rules:\
                    """.format(sg, 'xxx-xxx', "ca-central-1"))

            if protocol != row[1] or fromPort != row[2] or toPort != row[3]:
                protocol = row[1]
                fromPort = row[2]
                toPort = row[3]
                stype = ''
                port = ''
                if fromPort == toPort:
                    port = fromPort
                else:
                    port = "{0} - {1}".format(fromPort, toPort)

                with open("{0}/{1}.yml".format(directory, sg), "a") as f:
                    if protocol == "-1":
                        f.write("""
      - proto: all\
                        """)
                    else:
                        f.write("""
      - proto: {0}
        ports:
          - {1}\
                        """.format(protocol, port))

            if stype != row[4]:
                stype = row[4]
                with open("{0}/{1}.yml".format(directory, sg), "a") as f:
                    if stype == 1:
                        f.write("""
        cidr_ip:\
                        """)
                    elif stype == 2:
                        f.write("""
        group_name:\
                        """)

            source = ""
            if stype == 1:
                source = row[5]
            elif stype == 2:
                source = row[6]
            with open("{0}/{1}.yml".format(directory, sg), "a") as f:
                f.write("""
          - {0}\
                """.format(source))


