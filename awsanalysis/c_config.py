import yaml

class CConfig:
    def __init__(self):
        print("-> ConfigMgr init")
        self._conf = None
        self.loadConfig()

    def loadConfig(self):
        with open("config.yaml", "r") as ymlfile:
            conf = yaml.load(ymlfile)
        self._conf = conf.get("AwsAnalysis", {})

    def get(self, *args):
        return self._conf.get(*args)

