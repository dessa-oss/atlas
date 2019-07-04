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
        list_of_keys = _list_of_keys(first_key, len(first_value))
        return {key: value for key, value in zip(list_of_keys, first_value)}
    return param_dictionary

def _list_of_keys(key, length_of_list_value):
    return map(lambda list_index: '{}_{}'.format(key, list_index), range(length_of_list_value))

def _raw_json_from_parameters_file():
    with open('foundations_job_parameters.json', 'r') as parameters_file:
        return parameters_file.read()

def _parsed_json(file_contents):
    import json

    if file_contents == '':
        return {}
    else:
        return json.loads(file_contents)