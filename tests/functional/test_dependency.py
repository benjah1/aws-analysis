from awsanalysis.test.a_command_test import ACommandTest
import logging
from awsanalysis.a_loader import ALoader
from awsanalysis.a_analyzer import AAnalyzer

class A(ALoader):
    def dep(self):
        return set()
    def setup(self):
        print("sA")
    def load(self):
        print("lA")
class B(ALoader):
    def dep(self):
        return {"A"}
    def setup(self):
        print("sB")
    def load(self):
        print("lB")
class C(AAnalyzer):
    def dep(self):
        return {"A"}
    def analyze(self):
        print("aC")

class TestDependency(ACommandTest):
    def setup(self):
        super(TestDependency, self).setUp()

    def tearDown(self):
        super(TestDependency, self).tearDown()

    def test_dependency_loader_fail_run(self):
        cmdline = '-c ./tests/functional/config/dependency_loader_fail.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline, 1)

        self.assertIn("Error: Loader <A> not found for Loader <B>", stdout)

    def test_dependency_analyzer_run(self):
        cmdline = '-c ./tests/functional/config/dependency_analyzer.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("sA\nsB\nlA\nlB\naC\n", stdout)

    def test_dependency_analyzer_fail_run(self):
        cmdline = '-c ./tests/functional/config/dependency_analyzer_fail.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline, 1)

        self.assertIn("Error: Loader <A> not found for Analyzer <C>", stdout)

