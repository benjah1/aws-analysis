import unittest
import mock
import io
import contextlib
import logging
from awsanalysis.c_aws_analysis import CAwsAnalysis

class CapturedOutput(object):
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

@contextlib.contextmanager
def capture_output():
    stderr = io.StringIO()
    stdout = io.StringIO()
    with mock.patch('sys.stderr', stderr):
        with mock.patch('sys.stdout', stdout):
            yield CapturedOutput(stdout, stderr)

class ACommandTest(unittest.TestCase):
    def setUp(self):
        self.create_driver()

    def tearDown(self):
        return

    def create_driver(self):
        logging.debug("create driver")
        self.driver = CAwsAnalysis()

    def run_cmd(self, cmd, expected_rc=0):
        logging.debug("Calling cmd: %s", cmd)
        if not isinstance(cmd, list):
            cmdlist = cmd.split()
        else:
            cmdlist = cmd

        with capture_output() as captured:
            try:
                rc = self.driver.run(cmdlist)
            except SystemExit as e:
                # We need to catch SystemExit so that we
                # can get a proper rc and still present the
                # stdout/stderr to the test runner so we can
                # figure out what went wrong.
                rc = e.code
        stderr = captured.stderr.getvalue()
        stdout = captured.stdout.getvalue()
        self.assertEqual(
            rc, expected_rc,
            "Unexpected rc (expected: %s, actual: %s) for command: %s\n"
            "stdout:\n%sstderr:\n%s" % (
                expected_rc, rc, cmd, stdout, stderr))

        return stdout, stderr, rc

