import importlib
from abc import ABC, abstractmethod

class APluginMgr(ABC):
    def loadPlugin(self, pluginConf):
        _plugins = {}

        for obj in pluginConf:
            (clsName, conf), = obj.items()
            module = importlib.import_module(conf.get("pkg"), "")
            cls = getattr(module, clsName)
            _plugins[clsName] = cls(conf, self._dbMgr)

        return _plugins

    pass
