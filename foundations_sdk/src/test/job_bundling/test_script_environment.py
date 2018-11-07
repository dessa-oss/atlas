"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.job_bundling.script_environment import ScriptEnvironment

class TestScriptEnvironment(unittest.TestCase):

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
        self.assertEqual(['export offline_mode=OFFLINE\n'], self._written_lines)

    def test_write_environment_writes_multiple_exports(self):
        self._config['run_script_environment'] = {'log_level': 'DEBUG', 'offline_mode': 'OFFLINE'}
        self._environment.write_environment(self._file)
        self._orderless_array_match(['export log_level=DEBUG\n', 'export offline_mode=OFFLINE\n'], self._written_lines)

    def test_write_environment_handles_quoting(self):
        self._config['run_script_environment'] = {'log level': 'DEBUG THIS'}
        self._environment.write_environment(self._file)
        self.assertEqual(["export 'log level'='DEBUG THIS'\n"], self._written_lines)

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