from .a_plugin_mgr import APluginMgr
import logging

class CLoaderMgr(APluginMgr):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._loader = None
        self.init()
        self.sort()

    def init(self):
        conf = self._conf.get("loader", [])
        comm = self._conf.get("common", {})
        self._loader = self.loadPlugin(conf, comm)

        for name, loader in self._loader.items():
            loader.setup()

    def get(self, *args):
        return self._loader.get(*args)

    def sort(self):
        logging.debug("-> LoaderMgr sort")

    def load(self):
        for name, loader in self._loader.items():
            loader.load()

