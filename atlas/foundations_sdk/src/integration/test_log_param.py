
from foundations_spec import *

from foundations import log_param

class TestLogParam(Spec):

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

    @tear_down
    def tear_down(self):
        self._set_job_id(None)

    @skip
    def test_log_param_writes_params_to_redis(self):
        self._set_job_id('my_id')

        log_param('this_param', 'cool_value')
        log_param('that_param', 42)

        expected_loaded_parameters = {
            'this_param': 'cool_value',
            'that_param': 42
        }

        self._assert_flattened_parameter_keys_in_project_job_parameter_names_set('default', expected_loaded_parameters)
        self._assert_flattened_parameter_values_for_job_in_job_parameters('my_id', expected_loaded_parameters)
        self._assert_flattened_parameter_keys_in_project_input_parameter_names_set('default', expected_loaded_parameters)
        self._assert_flattened_parameter_names_for_job_in_job_input_parameters('my_id', expected_loaded_parameters)

    def _assert_flattened_parameter_keys_in_project_job_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_key: bytes(param_key, 'ascii'),flattened_parameters))
        logged_parameter_names = redis_connection.smembers('projects:{}:job_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_values_for_job_in_job_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        import json

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        logged_parameters = redis_connection.get('jobs:{}:parameters'.format(job_id))
        self.assertEqual(flattened_parameters, json.loads(logged_parameters))

    def _assert_flattened_parameter_keys_in_project_input_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_key: bytes(param_key, 'ascii'),flattened_parameters))
        logged_parameter_names = redis_connection.smembers('projects:{}:input_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_names_for_job_in_job_input_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection
        from foundations_internal.foundations_serializer import loads

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)

        flattened_parameters_data = []

        for parameter_name in flattened_parameters.keys():
            flattened_parameters_data.append({'argument': {'name': parameter_name, 'value': {'type': 'dynamic', 'name': parameter_name}}, 'stage_uuid': 'stageless'})

        logged_parameters = redis_connection.get('jobs:{}:input_parameters'.format(job_id))

        self.assertEqual(flattened_parameters_data, loads(logged_parameters))

    def _set_job_id(self, job_id):
        from foundations_contrib.global_state import current_foundations_context
        current_foundations_context().job_id = job_id