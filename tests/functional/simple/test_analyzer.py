from awsanalysis.a_analyzer import AAnalyzer

class TestAnalyzer(AAnalyzer):

    def dep(self):
        return ["TestLoader"]

    def analyze(self):
        print("analyze")

