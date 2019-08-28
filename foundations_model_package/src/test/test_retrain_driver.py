"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_model_package.retrain_driver import RetrainDriver

class TestRetrainDriver(Spec):

    @let
    def module_name(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.patch('builtins.open', self._mock_open)
        self._mock_files = {}

    def test_retrain_driver_generates_entrypoint_name(self):
        import re
        
        entrypoint_name_regex_string = '^retrain_driver_\d+\.py$'
        entrypoint_name_regex = re.compile(entrypoint_name_regex_string)
        
        with RetrainDriver(self.module_name, self.function_name) as entrypoint_name:
            self.assertIsNotNone(entrypoint_name_regex.match(entrypoint_name))

    def test_retrain_driver_generates_entrypoint_name_randomly(self):
        with RetrainDriver(self.module_name, self.function_name) as entrypoint_name:
            entrypoint_name_0 = entrypoint_name

        with RetrainDriver(self.module_name, self.function_name) as entrypoint_name:
            entrypoint_name_1 = entrypoint_name

        self.assertNotEqual(entrypoint_name_0, entrypoint_name_1)

    def test_retrain_driver_creates_driver_file(self):
        with RetrainDriver(self.module_name, self.function_name) as entrypoint_name:
            with open(entrypoint_name, 'r') as retrain_driver:
                self.assertEqual(self._expected_file_contents(), retrain_driver.read())

    def _expected_file_contents(self):
        return f'import foundations\nfrom {self.module_name} import {self.function_name}\n\nparams = foundations.load_parameters()\n{self.function_name}(**kwargs)\n'

    def _mock_open(self, file_name, mode):
        if mode == 'r':
            mock_file = self._mock_file()
            mock_file.read.return_value = self._mock_files[file_name]
        elif mode == 'w':
            mock_file = self._mock_file()
            mock_file.write.side_effect = self._mock_write(file_name)

        return mock_file

    def _mock_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda *args: mock_file
        mock_file.__exit__ = lambda *args: None

        return mock_file

    def _mock_write(self, file_name):
        if file_name not in self._mock_files:
            self._mock_files[file_name] = ''

        def _mock_write_callback(contents):
            self._mock_files[file_name] += contents

        return _mock_write_callback