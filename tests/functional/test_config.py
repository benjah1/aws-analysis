from awsanalysis.test.a_command_test import ACommandTest

class TestConfig(ACommandTest):
    def setup(self):
        super(TestConfig, self).setUp()

    def tearDown(self):
        super(TestConfig, self).tearDown()

    def test_config_wrong_param_run(self):
        cmdline = '-f ./tests/functional/config/simple.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline, 2)

        self.assertIn("-c <configurationfile>", stdout)

    def test_config_no_file_run(self):
        cmdline = '-c config_not_exist.yaml'
        stdout, stderr, rc = self.run_cmd(cmdline, 1)

        self.assertIn("Error: Config <config_not_exist.yaml> not found", stdout)

