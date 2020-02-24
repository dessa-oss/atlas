
import unittest

class TestQuarantine(unittest.TestCase):

    def test_run_test_with_quarantined_method_does_not_actually_run(self):
        test_run = self._run_fixture_test_suite('test_quarantine_method')
        self._assert_successful(test_run)
        self.assertIn('QuarantineWarning', test_run.stderr.decode())

    def test_run_test_with_quarantined_method_does_not_actually_run_setup_or_teardown(self):
        test_run = self._run_fixture_test_suite('test_quarantine_method_with_setup_and_teardown')
        self._assert_successful(test_run)
        self.assertIn('QuarantineWarning', test_run.stderr.decode())

    def test_run_test_with_quarantined_class_does_not_actually_run_setupclass_teardownclass_or_any_tests(self):
        test_run = self._run_fixture_test_suite('test_quarantine_class')
        self._assert_successful(test_run)
        self.assertIn('QuarantineWarning', test_run.stderr.decode())

    def _run_fixture_test_suite(self, fixture_name):
        import subprocess

        return subprocess.run(
            ['python', '-m', 'unittest', f'integration/fixtures/{fixture_name}.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def _assert_successful(self, process):
        returncode = process.returncode

        if process.returncode != 0:
            stdout = process.stdout.decode()
            stderr = process.stderr.decode()
            error_message = f'process returncode was not 0 (was {returncode}):\n   stdout: {stdout}\n    stderr: {stderr}'
            raise AssertionError(error_message)