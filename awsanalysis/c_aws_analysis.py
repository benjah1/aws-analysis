from .c_config import CConfig
from .c_loader_mgr import CLoaderMgr
from .c_analyzer_mgr import CAnalyzerMgr
from .c_db_mgr import CDBMgr
import getopt
import logging

class CAwsAnalysis:

    def __init__(self):
        self._conf = None
        self._loaderMgr = None
        self._analyzerMgr = None
        self._dbMgr = None
        self._configfile = None
 
    def run(self, argv):
        try:
            opts, args = getopt.getopt(argv,"c:",["config="])
        except getopt.GetoptError:
            print("-c <configurationfile>")
            return 2

        for opt, arg in opts:
            if opt == '-c':
                self._configfile = arg

        self.setup()
        self.load()
        self.analyze()
        return 0

    def setup(self):
        self._conf = CConfig(self._configfile)
        self._dbMgr = CDBMgr(self._conf)
        self._loaderMgr = CLoaderMgr(self._conf, self._dbMgr)
        self._analyzerMgr = CAnalyzerMgr(self._conf, self._dbMgr, self._loaderMgr)

        self._loaderMgr.setup()
        self._analyzerMgr.setup()

    def load(self):
        if self._conf.get('load', True):
            logging.debug("AwsAnalysis load")
            self._loaderMgr.load();

    def analyze(self):
        logging.debug("AwsAnalysis analyze")
        self._analyzerMgr.analyze();
