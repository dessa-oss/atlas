"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import * 
from foundations.parameters.generate_random_parameters import generate_random_parameters

class TestGenerateRandomParameters(Spec):
    
    @let
    def plain_parameters_dict(self):
        return {
            self.faker.word(): self.faker.random_int(),
            self.faker.word(): self.faker.pylist()
        }

    @let
    def min_max_parameter_search_space_dict(self):
        min_value = self.faker.random_int()

        return {
            self.faker.word(): {
                'min': min_value, 
                'max': min_value + self.faker.random_int()}
        }

    @let
    def min_count_max_count_parameter_search_space_dict(self):
        min_value = self.faker.random_int()
        min_count = self.faker.random_int()

        return {
            self.faker.word(): {
                'min': min_value, 
                'max': min_value + self.faker.random_int(), 
                'min_count': min_count, 
                'max_count': min_count + self.faker.random_int()
            }
        }

    @let
    def multiple_parameter_search_space_dict(self):
        min_value = self.faker.random_int()
        min_count = self.faker.random_int()

        return {
            self.faker.word(): {
                'min': min_value, 
                'max': min_value + self.faker.random_int(), 
                'min_count': min_count, 
                'max_count': min_count + self.faker.random_int()
            }, 
            self.faker.word(): {
                'min': min_value, 
                'max': min_value + self.faker.random_int()
            }
        }

    def test_generate_random_parameters_returns_empty_dict_when_given_empty_dict(self):
        self.assertEqual({}, generate_random_parameters({}))

    def test_generate_random_parameters_throws_error_when_given_non_dict_input(self):
        non_dict_input = self.faker.sentence()

        with self.assertRaises(TypeError) as e:
            generate_random_parameters(non_dict_input)

    def test_generate_random_parameters_returns_original_dict_when_search_space_not_provided(self):
        parameters_to_search = generate_random_parameters(self.plain_parameters_dict)
        self.assertEqual(parameters_to_search, self.plain_parameters_dict)
    
    def test_generate_random_parameters_returns_randomly_generated_parameters_when_given_valid_search_space_with_min_and_max(self):
        parameters_to_search = generate_random_parameters(self.min_max_parameter_search_space_dict)
        self._assert_generated_parameters_in_valid_range(parameters_to_search, self.min_max_parameter_search_space_dict)

    def test_generate_random_parameters_returns_randomly_generated_parameters_when_given_valid_search_space_with_min_count_and_max_count(self):
        parameters_to_search = generate_random_parameters(self.min_count_max_count_parameter_search_space_dict)
        self._assert_generated_parameters_in_valid_range(parameters_to_search, self.min_count_max_count_parameter_search_space_dict)
        self._assert_generated_parameters_length_in_valid_range(parameters_to_search, self.min_count_max_count_parameter_search_space_dict)

    def test_generate_random_parameters_returns_randomly_generated_parameters_when_given_multiple_valid_search_spaces(self):
        parameters_to_search = generate_random_parameters(self.multiple_parameter_search_space_dict)
        self._assert_generated_parameters_in_valid_range(parameters_to_search, self.multiple_parameter_search_space_dict)
        self._assert_generated_parameters_length_in_valid_range(parameters_to_search, self.multiple_parameter_search_space_dict)

    def _assert_generated_parameters_in_valid_range(self, generated_parameters, input_search_space):
        for param in input_search_space:
            if type(generated_parameters[param]) == list:
                for parameter_element in generated_parameters[param]:
                    self.assertTrue(input_search_space[param]['min'] <= parameter_element <= input_search_space[param]['max'])
            else:
                self.assertTrue(input_search_space[param]['min'] <= generated_parameters[param] <= input_search_space[param]['max'])

    def _assert_generated_parameters_length_in_valid_range(self, generate_random_parameters, input_search_space):
        for param in input_search_space:
            input_parameter_content = input_search_space[param]
            if type(input_parameter_content) == list:
                self.assertTrue(input_parameter_content['min_count'] <= len(generate_random_parameters) <= input_parameter_content['max_count'])