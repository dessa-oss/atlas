"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import numpy


def generate_random_parameters(parameter_search_space):
    if type(parameter_search_space) == dict:
        generated_params = {}

        for param in parameter_search_space:
            _generate_random_value_given_search_space(parameter_search_space, generated_params, param)

        return generated_params
    else:
        raise TypeError()


def _generate_random_value_given_search_space(parameter_search_space, generated_params, param):
    parameter_content = parameter_search_space[param]

    if type(parameter_content) == dict:
        if 'min' in parameter_content and 'max' in parameter_content:
            if 'min_count' in parameter_content and 'max_count' in parameter_content:
                minimum_list_length = parameter_content['min_count']
                maximum_list_length = parameter_content['max_count']
                list_length = numpy.random.randint(minimum_list_length, maximum_list_length)
                _generate_random_numbers_and_store(parameter_content, generated_params, param, list_length)
            else:
                _generate_random_numbers_and_store(parameter_content, generated_params, param, 1, False)

    if generated_params.get(param, None) == None:
        generated_params[param] = parameter_content


def _generate_random_numbers_and_store(parameter_content, generated_params, param, number_of_times, is_list=True):
    start = parameter_content['min']
    stop = parameter_content['max']

    if not is_list:
        generated_params[param] = numpy.random.uniform(start, stop)
    else:
        generated_params[param] = []
        for _ in range(number_of_times):
            generated_params[param].append(numpy.random.uniform(start, stop))
