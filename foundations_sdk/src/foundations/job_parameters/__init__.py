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
    flattened_output = {}

    for key, value in param_dictionary.items():
        if _is_scalar_value(value):
            flattened_output[key] = value
        elif isinstance(value, dict):
            flattened_output.update(_flatten_dict_value(key, value))
        else:
            flattened_output.update(_flatten_list_value(key, value))

    return flattened_output

def _is_scalar_value(value):
    return isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or value is None

def _flatten_dict_value(param_key, param_value):
    if not param_value:
        return {param_key: None}

    return {'{}_{}'.format(param_key, nested_key): nested_value for nested_key, nested_value in param_value.items()}

def _flatten_list_value(param_key, param_value):
    if not param_value:
        return {param_key: None}

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