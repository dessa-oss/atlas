"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.job_parameters import flatten_parameter_dictionary

class TestFlattenParameterDictionary(Spec):

    @let
    def random_key(self):
        return self.faker.word()

    @let
    def random_string_literal(self):
        return self.faker.word()

    def test_flatten_empty_dictionary_returns_empty_dictionary(self):
        parameter_input = {}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        self.assertEqual({}, flattened_parameter_input)

    def test_key_and_value_returns_key_and_value(self):
        parameter_input = {self.random_key: self.random_string_literal}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        self.assertEqual({self.random_key: self.random_string_literal}, flattened_parameter_input)