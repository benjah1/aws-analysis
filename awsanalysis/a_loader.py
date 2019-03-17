from abc import ABC, abstractmethod

class ALoader(ABC):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr
        self._dep = {}

    @abstractmethod
    def dep(self):
        raise NotImplementedError

    """
    should use db instead?
    def getDep(self, key):
        return self._loaderMgr.get(key)
    """

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

