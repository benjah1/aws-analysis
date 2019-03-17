from .a_plugin_mgr import APluginMgr
import logging

class CLoaderMgr(APluginMgr):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._loader = None

        # init plugin
        conf = self._conf.get("loader", [])
        comm = self._conf.get("common", {})
        self._loader = self.initPlugin(conf, comm)

    def setup(self):
        for name, loader in self._loader.items():
            loader.setup()
        self.sort()

    def sort(self):
        logging.debug("-> LoaderMgr sort")

    def load(self):
        for name, loader in self._loader.items():
            loader.load()

    def get(self, *args):
        return self._loader.get(*args)

