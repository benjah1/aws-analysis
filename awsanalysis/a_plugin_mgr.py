import importlib
from abc import ABC, abstractmethod

class APluginMgr(ABC):
    def loadPlugin(self, pluginConf, commonConf):
        _plugins = {}

        for obj in pluginConf:
            (clsName, conf), = obj.items()
            module = importlib.import_module(conf.get("pkg"), "")
            cls = getattr(module, clsName)
            finalConf = commonConf.copy()
            finalConf.update(conf)
            _plugins[clsName] = cls(finalConf, self._dbMgr)

        return _plugins

    pass
