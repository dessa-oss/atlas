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

    def random_literal_list(self):
        literal_list = []
        for _ in range(self.random_length):
            literal_list.append(self.faker.word())
        return literal_list

    @let
    def random_literal_list_value(self):
        return self.random_literal_list()

    @let
    def random_literal_dict_value(self):
        return {key: value for key, value in zip(self.random_literal_list(), self.random_literal_list())}

    @let
    def random_length(self):
        return self.faker.random_int(1, 10)
    
    @let
    def random_int(self):
        return self.faker.random_int(1,1000)

    @let
    def random_float(self):
        return self.faker.random.random() * 100

    def test_flatten_empty_dictionary_returns_empty_dictionary(self):
        parameter_input = {}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)
        
        self.assertEqual({}, flattened_parameter_input)

    def test_key_and_value_returns_key_and_value(self):
        parameter_input = {self.random_key: self.random_string_literal}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: self.random_string_literal}, flattened_parameter_input)

    def test_key_with_value_of_list_of_literals_returns_key_concatenated_with_list_index(self):
        parameter_input = {self.random_key: self.random_literal_list_value}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        list_of_keys = map(lambda list_index: '{}_{}'.format(self.random_key, list_index), range(self.random_length))
        expected_output = {key: value for key, value in zip(list_of_keys, self.random_literal_list_value)}

        self.assertEqual(expected_output, flattened_parameter_input)

    def test_key_with_value_int_returns_key_and_value(self):
        parameter_input = {self.random_key: self.random_int}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: self.random_int}, flattened_parameter_input)

    def test_key_with_value_float_returns_key_and_value(self):
        parameter_input = {self.random_key: self.random_float}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: self.random_float}, flattened_parameter_input)
    
    def test_key_with_value_none_returns_key_and_value(self):
        parameter_input = {self.random_key: None}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: None}, flattened_parameter_input)

    def test_key_with_value_empty_dict_turns_value_dict_into_none(self):
        parameter_input = {self.random_key: {}}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: None}, flattened_parameter_input)

    def test_key_with_value_empty_list_turns_value_dict_into_none(self):
        parameter_input = {self.random_key: []}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        self.assertEqual({self.random_key: None}, flattened_parameter_input)

    def test_key_with_value_of_dict_of_literals_returns_key_concatenated_with_nested_dict_keys(self):
        parameter_input = {self.random_key: self.random_literal_dict_value}
        flattened_parameter_input = flatten_parameter_dictionary(parameter_input)

        expected_output = {'{}_{}'.format(self.random_key, nested_key): nested_value for nested_key, nested_value in self.random_literal_dict_value.items()}
        self.assertEqual(expected_output, flattened_parameter_input)

    @skip
    def test_multiple_keys_with_at_most_singly_nested_values(self):
        none_literal_key = self.faker.word()
        int_literal_key = self.faker.word()
        float_literal_key = self.faker.word()
        string_literal_key = self.faker.word()
        non_empty_dictionary_key = self.faker.word()
        non_empty_list_key = self.faker.word()
        empty_dictionary_key = self.faker.word()
        empty_list_key = self.faker.word()

        parameter_input = {
            none_literal_key: None,
            int_literal_key: self.random_int,
            float_literal_key: self.random_float,
            string_literal_key: self.random_string_literal,
            empty_dictionary_key: {},
            empty_list_key: [],
            non_empty_list_key: self.random_literal_list_value,
            non_empty_dictionary_key: self.random_literal_dict_value
        }

        expected_output = {
            none_literal_key: None,
            int_literal_key: self.random_int,
            float_literal_key: self.random_float,
            string_literal_key: self.random_string_literal,
            empty_dictionary_key: None,
            empty_list_key: None
        }

        list_of_keys = map(lambda list_index: '{}_{}'.format(non_empty_list_key, list_index), range(self.random_length))
        list_output = {key: value for key, value in zip(list_of_keys, self.random_literal_list_value)}

        expected_output.update(list_output)

        expected_dict_output = {'{}_{}'.format(non_empty_dictionary_key, nested_key): nested_value for nested_key, nested_value in self.random_literal_dict_value.items()}

        expected_output.update(expected_dict_output)

        self.assertEqual(expected_output, flatten_parameter_dictionary(parameter_input))