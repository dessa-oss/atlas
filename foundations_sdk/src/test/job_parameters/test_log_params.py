"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations.job_parameters import log_params

class TestLogParams(Spec):

    mock_log_param = let_patch_mock('foundations.job_parameters.log_param')

    def mock_parameters_list(self):
        return self.faker.words()

    def mock_parameters_generator(self):
        keys = self.mock_parameters_list()
        values = self.mock_parameters_list()
        return {key: value for key, value in zip(keys, values)}

    @let
    def mock_parameters(self):
        return self.mock_parameters_generator()

    @let
    def mock_nested_parameters(self):
        return {
            self.faker.word(): self.mock_parameters_list(),
            self.faker.word(): self.mock_parameters_generator(),
            self.faker.word(): self.faker.random_int(1, 100)
        }

    def test_logs_nested_params_from_file_after_flattening(self):
        from foundations.job_parameters import flatten_parameter_dictionary

        log_params(self.mock_nested_parameters)

        for param_key, param_value in flatten_parameter_dictionary(self.mock_nested_parameters).items():
            self.mock_log_param.assert_any_call(param_key, param_value)