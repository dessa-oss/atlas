"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 02 2019
"""

from foundations_spec import *

class TestSetEnvironment(Spec):

    def test_missing_environment_raises_correct_error(self):
        _, error = self._run_script('missing_environment')
        self.assertIn('ValueError: No environment this-environment-does-not-exist found, please set a valid deployment environment with foundations.set_environment', error)

    def test_not_set_raises_correct_error(self):
        _, error = self._run_script('not_set')
        self.assertIn('ValueError: No environment found, please set deployment environments with foundations.set_environment', error)

    def test_valid_environment_runs_correctly(self):
        output, _ = self._run_script('valid_environment')
        self.assertIn('Finished stage', output)

    @staticmethod
    def _run_script(name):
        from subprocess import Popen, PIPE

        script = 'python acceptance/fixtures/set_environment/{}.py; true'.format(name)
        process = Popen(['bash', '-c', script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        return output.decode(), error.decode()
