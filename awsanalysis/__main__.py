import sys
from .c_aws_analysis import CAwsAnalysis

if __name__ == "__main__":
    awsAnalyzer = CAwsAnalysis()
    sys.exit(awsAnalyzer.run(sys.argv[1:]))

