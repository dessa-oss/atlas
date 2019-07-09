"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.parameters.generate_random_parameters import generate_random_parameters

class TestGenerateRandomParameters(Spec):

    def test_generate_random_parameters_returns_parameters_when_given_valid_input_dict(self):
        parameter_search_space = self._sample_parameter_dict()
        parameters_to_search = generate_random_parameters(parameter_search_space)

        self.assertTrue(parameter_search_space['learning_rate']['min'] <= parameters_to_search['learning_rate'] <= parameter_search_space['learning_rate']['max'])
        self.assertTrue(parameter_search_space['layer_shapes']['min_count'] <= len(parameters_to_search['layer_shapes']) <= parameter_search_space['layer_shapes']['max_count'])
        for value in parameters_to_search['layer_shapes']:
            self.assertTrue(parameter_search_space['layer_shapes']['min'] <= value <= parameter_search_space['layer_shapes']['max'])

    def _sample_parameter_dict(self):
        parameter_search_space = {
            'learning_rate': {
                'min': 0.0001, 'max': 0.001
            },
            'layer_shapes': {
                'min': 600, 'max': 3084, 'min_count': 1, 'max_count': 3
            }
        }
        return parameter_search_space