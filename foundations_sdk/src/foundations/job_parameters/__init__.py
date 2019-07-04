"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def load_parameters():
    try:
        return _parsed_json(_raw_json_from_parameters_file())
    except FileNotFoundError:
        return {}

def flatten_parameter_dictionary(param_dictionary):
    if param_dictionary:
        first_key = list(param_dictionary)[0]
        first_value = param_dictionary[first_key]
        if isinstance(first_value, str):
            return param_dictionary
        if isinstance(first_value, int):
            return param_dictionary
        return _flatten_list_value(first_key, first_value)
    return param_dictionary

def _flatten_list_value(param_key, param_value):
    list_of_keys = _list_of_keys(param_key, len(param_value))
    return {key: value for key, value in zip(list_of_keys, param_value)}

def _list_of_keys(key, length_of_list_value):
    return ['{}_{}'.format(key, list_index) for list_index in range(length_of_list_value)]

def _raw_json_from_parameters_file():
    with open('foundations_job_parameters.json', 'r') as parameters_file:
        return parameters_file.read()

def _parsed_json(file_contents):
    import json

    if file_contents == '':
        return {}
    else:
        return json.loads(file_contents)