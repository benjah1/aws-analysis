import yaml

class CConfig:
    def __init__(self, configfile):
        self._conf = None
        self.loadConfig(configfile)

    def loadConfig(self, configfile):
        if not configfile:
            configfile = "config.yaml"
        with open(configfile, "r") as ymlfile:
            conf = yaml.load(ymlfile)
        self._conf = conf.get("AwsAnalysis", {})

    def get(self, *args):
        return self._conf.get(*args)

