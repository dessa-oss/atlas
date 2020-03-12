from foundations_spec import *
from acceptance.mixins.run_local_job import RunLocalJob
from acceptance.mixins.run_with_default_foundations_home import RunWithDefaultFoundationsHome

class TestCanLoadParameters(Spec, RunLocalJob, RunWithDefaultFoundationsHome):

    @let
    def redis_connection(self):
        import os

        if os.getenv('RUNNING_ON_CI', False):
            import redis
            return redis.Redis(host=os.environ['LOCAL_DOCKER_SCHEDULER_HOST'], port='5556')

        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @let
    def job_parameters(self):
        import json
        with open(self.script_directory + '/foundations_job_parameters.json', 'r') as file:
            return json.load(file)

    @let
    def project_name(self):
        return self.faker.word().lower()

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

    @set_up_class
    def set_up_class(klass):
        pass

    @set_up
    def set_up(self):
        import subprocess
        import os

        with self.unset_foundations_home():
            env = self._update_environment_with_home_directory() if os.getenv('RUNNING_ON_CI', False) else {}
            env = {**os.environ, **env}
            subprocess.run(f'python -m foundations login http://{os.getenv("LOCAL_DOCKER_SCHEDULER_HOST", "localhost")}:5558 -u test -p test'.split(' '), env=env)

    def test_can_load_parameters_within_python(self):
        self._test_can_load_parameters_within_python(self.script_directory, self.job_parameters, check_for_warning=True)

    def test_can_load_parameters_within_foundations_submit(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory, self.job_parameters)

    def test_can_load_parameters_as_empty_dict_within_python_empty_params(self):
        self._test_can_load_parameters_within_python(self.script_directory_empty_params, {})

    def test_can_load_parameters_as_empty_dict_within_foundations_submit_empty_params(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory_empty_params, {})

    def test_can_load_default_parameters_within_foundations_submit_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory_no_parameters, {})

    def test_can_load_default_parameters_within_python_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_python(self.script_directory_no_parameters, {})

    def _test_can_load_parameters_within_python(self, script_directory, expected_loaded_parameters, check_for_warning=False):
        self._test_command_that_loads_parameters_in_directory_for_python(['python', 'main.py'], script_directory, expected_loaded_parameters, check_for_warning)

    def _test_can_load_parameters_within_foundations_submit(self, script_directory, expected_loaded_parameters):
        self._test_command_that_loads_parameters_in_directory(['python', '-m', 'foundations', 'submit','--project-name', self.project_name, 'scheduler', '.', 'project_code/script_to_run.py'], script_directory, expected_loaded_parameters)

    def _test_command_that_loads_parameters_in_directory(self, command, script_directory, expected_loaded_parameters):
        from foundations_internal.change_directory import ChangeDirectory

        import subprocess
        import json
        import os
        import os.path as path

        with self.unset_foundations_home():
            env = self._update_environment_with_home_directory() if os.getenv('RUNNING_ON_CI', False) else {}
            env = {**os.environ, **env}

            with ChangeDirectory(script_directory):
                completed_process = subprocess.run(command, stdout=subprocess.PIPE, env=env)
                process_output = completed_process.stdout.decode().strip().split('\n')
                print(process_output)

            if os.getenv('RUNNING_ON_CI', False):
                import re
                from foundations_local_docker_scheduler_plugin.job_deployment import JobDeployment
                from foundations_contrib.global_state import config_manager

                job_id_regex = re.search('Job \'(.+?)\' has completed.', process_output[-1])
                self.assertIsNotNone(job_id_regex)
                job_id = job_id_regex.group(1)

                # Creating a fake job deployment as a quick interface to grab its logs
                config_manager.config()['scheduler_url'] = f"http://{os.environ['LOCAL_DOCKER_SCHEDULER_HOST']}:5000"
                job = JobDeployment(job_id, None, None)
                process_output = job.get_job_logs().split('\n')

            params_json = process_output[-2]
            job_id = process_output[-3]
            project_name = self.project_name
            result_parameters = json.loads(params_json)

            self.assertEqual(expected_loaded_parameters, result_parameters)
            self._assert_flattened_parameter_keys_in_project_job_parameter_names_set(project_name, expected_loaded_parameters)
            self._assert_flattened_parameter_values_for_job_in_job_parameters(job_id, expected_loaded_parameters)
            self._assert_flattened_parameter_keys_in_project_input_parameter_names_set(project_name, expected_loaded_parameters)
            if expected_loaded_parameters:
                self._assert_flattened_parameter_names_for_job_in_job_input_parameters(job_id, expected_loaded_parameters)

    def _test_command_that_loads_parameters_in_directory_for_python(self, command, script_directory, expected_loaded_parameters, check_for_warning):
        from foundations_internal.change_directory import ChangeDirectory

        import subprocess
        import json
        import os.path as path

        env = self._update_environment_with_home_directory()

        with ChangeDirectory(script_directory):
            env = None if check_for_warning else env
            completed_process = subprocess.run(command, stdout=subprocess.PIPE, env=env)
            process_output = completed_process.stdout.decode()

        warnings, _, params_json = process_output.strip().rpartition('\n')
        if check_for_warning:
            self.assertIn('Script not run with Foundations.', warnings)

        result_parameters = json.loads(params_json)
        self.assertEqual(expected_loaded_parameters, result_parameters)

    def _assert_flattened_parameter_keys_in_project_job_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_name: bytes(param_name, 'ascii'), flattened_parameters))
        logged_parameter_names = self.redis_connection.smembers('projects:{}:job_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_values_for_job_in_job_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        import json

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)

        parameters_in_redis = self.redis_connection.get('jobs:{}:parameters'.format(job_id))

        if parameters_in_redis is None:
            logged_parameters = {}
        else:
            logged_parameters = json.loads(parameters_in_redis)

        self.assertEqual(flattened_parameters, logged_parameters)

    def _assert_flattened_parameter_keys_in_project_input_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_key: bytes(param_key, 'ascii'),flattened_parameters))
        logged_parameter_names = self.redis_connection.smembers('projects:{}:input_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_names_for_job_in_job_input_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_internal.foundations_serializer import loads

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)

        flattened_parameters_data = []

        for parameter_name in flattened_parameters.keys():
            flattened_parameters_data.append({'argument': {'name': parameter_name, 'value': {'type': 'dynamic', 'name': parameter_name}}, 'stage_uuid': 'stageless'})

        logged_parameters = self.redis_connection.get('jobs:{}:input_parameters'.format(job_id))
        self.assertEqual(flattened_parameters_data, loads(logged_parameters))