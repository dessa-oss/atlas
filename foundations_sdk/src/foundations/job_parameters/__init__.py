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

def log_param(key, value):
    from foundations_contrib.global_state import redis_connection, current_foundations_context

    foundations_context = current_foundations_context()
    project_name = foundations_context.project_name()
    job_id = foundations_context.job_id()

    _insert_parameter_name_into_projects_params_set(redis_connection, project_name, key)
    _insert_parameter_value_into_job_run_data(redis_connection, job_id, key, value)

def _insert_parameter_name_into_projects_params_set(redis_connection, project_name, key):
    redis_connection.sadd(f'projects:{project_name}:job_parameter_names', key)

def _insert_parameter_value_into_job_run_data(redis_connection, job_id, key, value):
    import json

    job_params_key = f'jobs:{job_id}:parameters'

    serialized_job_params = redis_connection.get(job_params_key)
    job_params = _deserialized_job_params(serialized_job_params)

    job_params[key] = value

    redis_connection.set(job_params_key, json.dumps(job_params))

def _deserialized_job_params(serialized_job_params):
    import json

    if serialized_job_params is None:
        return {}
    else:
        return json.loads(serialized_job_params)

def _is_scalar_value(value):
    return isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or value is None

def _flatten_dict_value(param_key, param_value):
    if not param_value:
        return {param_key: None}

    return flatten_parameter_dictionary({'{}_{}'.format(param_key, nested_key): nested_value for nested_key, nested_value in param_value.items()})

def _flatten_list_value(param_key, param_value):
    if not param_value:
        return {param_key: None}

    list_of_keys = _list_of_keys(param_key, len(param_value))
    return flatten_parameter_dictionary({key: value for key, value in zip(list_of_keys, param_value)})

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