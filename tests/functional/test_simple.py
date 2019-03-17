from awsanalysis.test.a_command_test import ACommandTest
import logging

class TestSimple(ACommandTest):
    def setup(self):
        super(TestSimple, self).setUp()
        # self.files = FileCreator()

    def tearDown(self):
        super(TestSimple, self).tearDown()

    def test_simple_run(self):
        cmdline = '-c ./tests/functional/simple/config.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline)

        self.assertIn("setup\nload\nanalyze", stdout)
