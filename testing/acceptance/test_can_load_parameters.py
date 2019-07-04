"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

@skip
class TestCanLoadParameters(Spec):

    @let
    def job_parameters(self):
        import json
        with open(self.script_directory + '/foundations_job_parameters.json', 'r') as file:
            return json.load(file)

    @let
    def script_directory(self):
        return 'acceptance/fixtures/script_parameters'

    @let
    def script_directory_no_parameters(self):
        return 'acceptance/fixtures/script_parameters_no_parameters'

    @let
    def deployable_script_directory(self):
        return 'acceptance/fixtures/deployable_script_parameters'

    @let
    def deployable_script_directory_no_parameters(self):
        return 'acceptance/fixtures/deployable_script_parameters_no_parameters'

    @let
    def script_directory_empty_params(self):
        return 'acceptance/fixtures/script_parameters_empty_params'

    @let
    def deployable_script_directory_empty_params(self):
        return 'acceptance/fixtures/deployable_script_parameters_empty_params'

    def test_can_load_parameters_within_python(self):
        self._test_can_load_parameters_within_python(self.script_directory, self.job_parameters)

    def test_can_load_parameters_within_foundations_deploy(self):
        self._test_can_load_parameters_within_foundations_deploy(self.deployable_script_directory, self.job_parameters)

    def test_can_load_parameters_as_empty_dict_within_python_empty_params(self):
        self._test_can_load_parameters_within_python(self.script_directory_empty_params, {})

    def test_can_load_parameters_as_empty_dict_within_foundations_deploy_empty_params(self):
        self._test_can_load_parameters_within_foundations_deploy(self.deployable_script_directory_empty_params, {})

    def test_can_load_default_parameters_within_foundations_deploy_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_foundations_deploy(self.deployable_script_directory_no_parameters, {})

    def test_can_load_default_parameters_within_python_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_python(self.script_directory_no_parameters, {})

    def _test_can_load_parameters_within_python(self, script_directory, expected_loaded_parameters):
        self._test_command_that_loads_parameters_in_directory(['python', 'main.py'], script_directory, expected_loaded_parameters)

    def _test_can_load_parameters_within_foundations_deploy(self, script_directory, expected_loaded_parameters):
        self._test_command_that_loads_parameters_in_directory(['python', '-m', 'foundations', 'deploy', '--env', 'local', '--entrypoint', 'project_code/script_to_run.py'], script_directory, expected_loaded_parameters)

    def _test_command_that_loads_parameters_in_directory(self, command, script_directory, expected_loaded_parameters):
        from foundations_internal.change_directory import ChangeDirectory

        import subprocess
        import json
        import os.path as path

        with ChangeDirectory(script_directory):
            completed_process = subprocess.run(command, stdout=subprocess.PIPE)
            process_output = completed_process.stdout

        result_parameters = json.loads(process_output)
        self.assertEqual(expected_loaded_parameters, result_parameters)
        self._assert_flattened_parameter_keys_in_project_job_parameter_names_set(path.basename(script_directory), expected_loaded_parameters)

    def _assert_flattened_parameter_keys_in_project_job_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(flattened_parameters)
        logged_parameter_names = redis_connection.smembers('projects:{}:job_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_values_for_job_in_job_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        import json

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        logged_parameters = redis_connection.get('jobs:{}:parameters'.format(job_id))
        self.assertEqual(flattened_parameters, json.loads(logged_parameters))