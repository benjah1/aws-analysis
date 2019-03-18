from .a_plugin_mgr import APluginMgr
from toposort import toposort_flatten
import logging

class CLoaderMgr(APluginMgr):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._loader = None
        self._order = None

        # init plugin
        conf = self._conf.get("loader", [])
        comm = self._conf.get("common", {})
        self._loader = self.initPlugin(conf, comm)

    def setup(self):
        for name, loader in self._loader.items():
            loader.setup()
        self.sort()

    def sort(self):
        data = {}
        # check dependency
        for name, loader in self._loader.items():
            dep = loader.dep()
            for check in dep:
                if not self.get(check, None):
                    raise Exception("Loader <{}> not found for Loader <{}>".format(check, name))
            data[name] = dep

        self._order = toposort_flatten(data)

    def load(self):
        for name in self._order:
            self.get(name).load()

    def get(self, *args):
        return self._loader.get(*args)

