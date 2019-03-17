from .a_plugin_mgr import APluginMgr
import logging

class CAnalyzerMgr(APluginMgr):
    def __init__(self, conf, dbMgr, loaderMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._loaderMgr = loaderMgr
        self._analyzer = None

        # init plugin
        conf = self._conf.get("analyzer", [])
        comm = self._conf.get("common", {})
        self._analyzer = self.initPlugin(conf, comm)

    def setup(self):
        # check dependency
        logging.debug("todo")

    def analyze(self):
        for name, analyzer in self._analyzer.items():
            analyzer.analyze()
        
