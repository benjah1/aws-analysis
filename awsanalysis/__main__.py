import sys
from .c_aws_analysis import CAwsAnalysis

if __name__ == "__main__":
    print("this is main")
    awsAnalyzer = CAwsAnalysis()
    sys.exit(awsAnalyzer.run())

