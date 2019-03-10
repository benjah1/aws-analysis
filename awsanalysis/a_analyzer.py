from abc import ABC, abstractmethod

class AAnalyzer(ABC):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr

    @abstractmethod
    def dep(self):
        pass

    @abstractmethod
    def analyze(self):
        pass

