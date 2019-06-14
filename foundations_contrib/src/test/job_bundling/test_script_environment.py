"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.job_bundling.script_environment import ScriptEnvironment

class TestScriptEnvironment(Spec):

    @let
    def redis_password(self):
        return self.faker.word()

    def setUp(self):
        self._config = {}
        self._environment = ScriptEnvironment(self._config)
        self._written_lines = []
        self._file = Mock(**{'write.side_effect': self._write})

    def test_write_environment_writes_empty_export(self):
        self._environment.write_environment(self._file)
        self.assertEqual([], self._written_lines)

    def test_write_environment_writes_single_export(self):
        self._config['run_script_environment'] = {'log_level': 'DEBUG'}
        self._environment.write_environment(self._file)
        self.assertEqual(['export log_level=DEBUG\n'], self._written_lines)

    def test_write_environment_writes_single_export_different_values(self):
        self._config['run_script_environment'] = {'offline_mode': 'OFFLINE'}
        self._environment.write_environment(self._file)
        self.assertEqual(['export offline_mode=OFFLINE\n'],
                         self._written_lines)

    def test_write_environment_writes_multiple_exports(self):
        self._config['run_script_environment'] = {'log_level': 'DEBUG', 'offline_mode': 'OFFLINE'}
        self._environment.write_environment(self._file)
        self._orderless_array_match(
            ['export log_level=DEBUG\n', 'export offline_mode=OFFLINE\n'], self._written_lines)

    def test_write_environment_handles_quoting(self):
        self._config['run_script_environment'] = {'log level': 'DEBUG THIS'}
        self._environment.write_environment(self._file)
        self.assertEqual(
            ["export 'log level'='DEBUG THIS'\n"], self._written_lines)

    def test_write_environment_adds_redis_password_if_any(self):
        attributes = ConditionalReturn()
        attributes.return_when(self.redis_password, 'FOUNDATIONS_REDIS_PASSWORD')
        self.patch('os.environ.get', attributes)
        self._environment.write_environment(self._file)
        self.assertEqual(['export FOUNDATIONS_REDIS_PASSWORD={}\n'.format(self.redis_password)], self._written_lines)

    def test_write_environment_adds_redis_password_if_any_and_any_other_run_script_environment_stuff(self):
        self._config['run_script_environment'] = {'log level': 'DEBUG THIS'}

        attributes = ConditionalReturn()
        attributes.return_when(self.redis_password, 'FOUNDATIONS_REDIS_PASSWORD')
        self.patch('os.environ.get', attributes)

        self._environment.write_environment(self._file)
        self.assertEqual(['export FOUNDATIONS_REDIS_PASSWORD={}\n'.format(self.redis_password), "export 'log level'='DEBUG THIS'\n"], self._written_lines)

    def test_write_environment_flushes_file(self):
        self._environment.write_environment(self._file)
        self._file.flush.assert_called()

    def test_write_environment_rewinds_file(self):
        self._environment.write_environment(self._file)
        self._file.seek.assert_called_with(0)

    def _orderless_array_match(self, lhs, rhs):
        equal = len(lhs) == len(rhs)
        for item in lhs:
            equal = equal and item in rhs
        return equal

    def _write(self, value):
        self._written_lines.append(value)
