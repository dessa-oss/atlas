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

    @let
    def function_kwargs(self):
        return self.faker.pydict()

    def test_retrain_driver_generates_entrypoint_name(self):
        import re
        
        entrypoint_name_regex_string = '^retrain_driver_\d+\.py$'
        entrypoint_name_regex = re.compile(entrypoint_name_regex_string)
        
        with RetrainDriver(self.module_name, self.function_name, self.function_kwargs) as entrypoint_name:
            self.assertIsNotNone(entrypoint_name_regex.match(entrypoint_name))