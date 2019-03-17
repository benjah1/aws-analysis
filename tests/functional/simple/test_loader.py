from awsanalysis.a_loader import ALoader

class TestLoader(ALoader):
    def dep(self):
        return []

    def setup(self):
        print("setup")

    def load(self):
        print("load")

