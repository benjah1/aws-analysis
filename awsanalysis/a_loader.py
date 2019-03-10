from abc import ABC, abstractmethod

class ALoader(ABC):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._dep = {}

    @abstractmethod
    def dep(self):
        pass

    """
    should use db instead?
    def getDep(self, key):
        return self._loaderMgr.get(key)
    """

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def load(self):
        pass

