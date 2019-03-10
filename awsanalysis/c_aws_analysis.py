from .c_config import CConfig
from .c_loader_mgr import CLoaderMgr
from .c_analyzer_mgr import CAnalyzerMgr
from .c_db_mgr import CDBMgr

class CAwsAnalysis:

    def __init__(self):
        self._conf = None
        self._loaderMgr = None
        self._analyzerMgr = None
        self._dbMgr = None
 
    def run(self):
        print("this is cAwsAnalyzer")
        self.setup()
        self.load()
        self.analyze()

    def setup(self):
        print("AwsAnalysis init config mgr")
        self._conf = CConfig()

        print("AwsAnalysis init db mgr")
        self._dbMgr = CDBMgr(self._conf)

        print("AwsAnalysis init loader mgr")
        self._loaderMgr = CLoaderMgr(self._conf, self._dbMgr)

        print("AwsAnalysis init analyzer mgr")
        self._analyzerMgr = CAnalyzerMgr(self._conf, self._dbMgr, self._loaderMgr)

    def load(self):
        if self._conf.get('load', True):
            print("AwsAnalysis load")
            self._loaderMgr.load();

    def analyze(self):
        print("AwsAnalysis analyze")
        self._analyzerMgr.analyze();
