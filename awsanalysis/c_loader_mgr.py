from .a_plugin_mgr import APluginMgr

class CLoaderMgr(APluginMgr):
    def __init__(self, conf, dbMgr):
        print("-> LoaderMgr init")
        self._conf = conf
        self._dbMgr = dbMgr
        self._loader = None
        self.init()
        self.sort()

    def init(self):
        conf = self._conf.get("loader", [])
        self._loader = self.loadPlugin(conf)
        print(self._loader)

        for name, loader in self._loader.items():
            loader.setup()

    def get(self, *args):
        return self._loader.get(*args)

    def sort(self):
        print("-> LoaderMgr sort")

    def load(self):
        print("-> LoaderMgr load")
        for name, loader in self._loader.items():
            loader.load()

