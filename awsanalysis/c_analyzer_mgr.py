from .a_plugin_mgr import APluginMgr

class CAnalyzerMgr(APluginMgr):
    def __init__(self, conf, dbMgr, loaderMgr):
        print("-> AnalyzerMgr init")
        self._conf = conf
        self._dbMgr = dbMgr
        self._loaderMgr = loaderMgr
        self._analyzer = None
        self.init()
        self.checkDep()

    def init(self):
        conf = self._conf.get("analyzer", [])
        self._analyzer = self.loadPlugin(conf)

    def checkDep(self):
        print("todo")

    def analyze(self):
        print("-> AnalyzerMgr analyze")
        for name, analyzer in self._analyzer.items():
            analyzer.analyze()
        
