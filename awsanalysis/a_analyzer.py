from abc import ABC, abstractmethod

class AAnalyzer(ABC):
    def __init__(self, conf, dbMgr):
        self._conf = conf
        self._dbMgr = dbMgr

    @abstractmethod
    def dep(self): 
        raise NotImplementedError

    @abstractmethod
    def analyze(self): 
        raise NotImplementedError

