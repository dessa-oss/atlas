"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from test.mixin.mock_file_system import MockFileSystem

from foundations_model_package.retrain_driver import RetrainDriver

class TestRetrainDriver(Spec, MockFileSystem):

    @let
    def module_name(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self._set_up_mocks()

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
                self.assertEqual(self._expected_file_contents(entrypoint_name), retrain_driver.read())

    def test_retrain_driver_deletes_driver_file_on_exit(self):
        import os.path as path

        with RetrainDriver(self.module_name, self.function_name) as entrypoint_name:
            entrypoint_script_name = entrypoint_name

        self.assertFalse(path.isfile(entrypoint_script_name))

    def _expected_file_contents(self, entrypoint_name):
        return f'import os\n\nimport foundations\nfrom {self.module_name} import {self.function_name}\n\nparams = foundations.load_parameters()\n{self.function_name}(**params)\nos.remove({entrypoint_name})\n'
