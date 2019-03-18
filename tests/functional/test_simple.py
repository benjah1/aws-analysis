from awsanalysis.test.a_command_test import ACommandTest
import logging
from awsanalysis.a_loader import ALoader
from awsanalysis.a_analyzer import AAnalyzer

class TestLoader(ALoader):
    def dep(self):
        return set()
    def setup(self):
        print("setup")
    def load(self):
        print("load")

class TestAnalyzer(AAnalyzer):
    def dep(self):
        return {"TestLoader"}
    def analyze(self):
        print("analyze")

class TestSimple(ACommandTest):
    def setup(self):
        super(TestSimple, self).setUp()

    def tearDown(self):
        super(TestSimple, self).tearDown()

    def test_simple_run(self):
        cmdline = '-c ./tests/functional/config/simple.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("setup\nload\nanalyze", stdout)

    def test_simple_no_load_run(self):
        cmdline = '-c ./tests/functional/config/simple_no_load.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("setup\nanalyze", stdout)

