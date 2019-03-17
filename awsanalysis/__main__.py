import sys
import logging
import os
from .c_aws_analysis import CAwsAnalysis

if __name__ == "__main__":
    LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
    logging.basicConfig(level=LOGLEVEL)
    awsAnalyzer = CAwsAnalysis()
    sys.exit(awsAnalyzer.run(sys.argv[1:]))

