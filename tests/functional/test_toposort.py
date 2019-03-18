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
        return {"C", "A"}
    def setup(self):
        print("sB")
    def load(self):
        print("lB")
class C(ALoader):
    def dep(self):
        return {"A"}
    def setup(self):
        print("sC")
    def load(self):
        print("lC")
class D(ALoader):
    def dep(self):
        return {"C", "A"}
    def setup(self):
        print("sD")
    def load(self):
        print("lD")
class E(ALoader):
    def dep(self):
        return {"F"}
    def setup(self):
        print("sE")
    def load(self):
        print("lE")
class F(ALoader):
    def dep(self):
        return {"E"}
    def setup(self):
        print("sF")
    def load(self):
        print("lF")


class TestToposort(ACommandTest):
    def setup(self):
        super(TestToposort, self).setUp()

    def tearDown(self):
        super(TestToposort, self).tearDown()

    def test_toposort_run(self):
        cmdline = '-c ./tests/functional/config/toposort.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("sA\nsB\nsC\nlA\nlC\nlB\n", stdout)

    def test_toposort_identical_run(self):
        # loader with identical dependency
        cmdline = '-c ./tests/functional/config/toposort_identical.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("sA\nsB\nsC\nsD\nlA\nlC\nlB\nlD\n", stdout)

    def test_toposort_circle_run(self):
        cmdline = '-c ./tests/functional/config/toposort_circle.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline, 1)

        self.assertIn("Error: Circular", stdout)

