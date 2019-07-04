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

    @let
    def random_literal_list(self):
        literal_list = []
        for _ in range(self.random_length):
            literal_list.append(self.faker.word())
        return literal_list

    @let
    def random_length(self):
        return self.faker.random_int(1, 10)

    def test_flatten_empty_dictionary_returns_empty_dictionary(self):
        parameter_input = {}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        self.assertEqual({}, flattened_parameter_input)

    def test_key_and_value_returns_key_and_value(self):
        parameter_input = {self.random_key: self.random_string_literal}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        self.assertEqual({self.random_key: self.random_string_literal}, flattened_parameter_input)

    def test_key_with_value_of_list_of_literals_returns_key_concatenated_with_list_index(self):
        parameter_input = {self.random_key: self.random_literal_list}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        list_of_keys = map(lambda list_index: '{}_{}'.format(self.random_key, list_index), range(self.random_length))
        expected_output = {key: value for key, value in zip(list_of_keys, self.random_literal_list)}
        self.assertEqual(expected_output, flattened_parameter_input)