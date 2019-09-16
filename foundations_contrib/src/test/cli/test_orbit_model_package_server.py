"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import pickle
import base64
import stat
from foundations_spec import *
import foundations_contrib
import fakeredis


class TestOrbitModelPackageServer(Spec):

    mock_time = let_patch_mock('time.time')

    @let
    def mock_project_name(self):
        return self.faker.word()

    @let
    def mock_2nd_project_name(self):
        return self.faker.word()

    @let
    def mock_model_name(self):
        return self.faker.word()

    @let
    def mock_2nd_model_name(self):
        return self.faker.word()

    @let
    def mock_project_directory(self):
        return self.faker.uri_path()

    @let
    def model_information(self):
        return {
            'status': 'activated',
            'default': True,
            'created_by': '',
            'created_at': self.mock_time(),
            'description': '',
            'entrypoints': {},
            'validation_metrics': {}
        }

    @let
    def decoded_key(self):
        return bytes(self.faker.sentence(), 'utf-8')

    @let
    def secret_key(self):
        return base64.b64encode(self.decoded_key)

    @let
    def mock_expected_yaml(self):
        import yaml
        return yaml.dump({
            'apiVersion': 'v1',
            'kind': 'Secret',
            'data': {
                'job-uploader': self.secret_key
            }
        })

    @set_up
    def set_up(self):
        import os.path as path

        self.maxDiff=None
        
        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())
        self._redis.flushall()
        self._redis.execute_command = lambda x: x 
        

        self.ssh_key_path = path.expanduser('~/.ssh/id_foundations_scheduler')
        self.mock_redis_execute_command = self.patch('foundations_contrib.global_state.redis_connection.execute_command')
        self._setup_mocks_for_config_retrival()

        self.mock_time.return_value = 10


    def _mock_enter(self, *args):
        return self.mock_ssh_file

    def _mock_exit(self, *args):
        pass

    def _setup_mocks_for_config_retrival(self):
        self.mock_syncable_directories = self.patch('foundations.artifacts.syncable_directory.SyncableDirectory')
        self.mock_foundations_set_environment = self.patch('foundations.set_environment')
        
        self.mock_ssh_file = Mock()
        
        self.mock_open = self.patch('builtins.open', ConditionalReturn())
        self.mock_open.return_when(self.mock_ssh_file, self.ssh_key_path, 'w+b')


        self.mock_subprocess_run_with_return = self.patch('subprocess.run', ConditionalReturn())
        mock_subprocess_object = Mock()
        mock_subprocess_object.stdout = self.mock_expected_yaml
        
        self.mock_subprocess_object_for_deploy = Mock()
        self.mock_subprocess_object_for_deploy.returncode = 0

        self.mock_subprocess_object_for_destroy = Mock()
        self.mock_subprocess_object_for_destroy.returncode = 0

        mock_path_exists = self.patch('os.path.exists', ConditionalReturn())
        mock_path_exists.return_when(True, self.ssh_key_path)

        self.mock_ssh_file.__enter__ = self._mock_enter
        self.mock_ssh_file.__exit__ = self._mock_exit

        self.patch('os.chmod')
        self.patch('os.remove')
        
        import subprocess
        
        self.mock_subprocess_run_with_return.return_when(mock_subprocess_object, ['bash', '-c', 'kubectl -n foundations-scheduler-test get secret job-server-private-keys -o yaml'], stdout=subprocess.PIPE)
        self.mock_subprocess_run_with_return.return_when(self.mock_subprocess_object_for_deploy, ['bash', './deploy_serving.sh', self.mock_project_name, self.mock_model_name, 'none'],cwd=foundations_contrib.root() / 'resources/model_serving/orbit')
        self.mock_subprocess_run_with_return.return_when(self.mock_subprocess_object_for_deploy, ['bash', './deploy_serving.sh', self.mock_project_name, self.mock_2nd_model_name, 'none'],cwd=foundations_contrib.root() / 'resources/model_serving/orbit')
        self.mock_subprocess_run_with_return.return_when(self.mock_subprocess_object_for_deploy, ['bash', './deploy_serving.sh', self.mock_2nd_project_name, self.mock_model_name, 'none'],cwd=foundations_contrib.root() / 'resources/model_serving/orbit')
        self.mock_subprocess_run_with_return.return_when(self.mock_subprocess_object_for_destroy, ['bash', './remove_deployment.sh', self.mock_project_name, self.mock_model_name, 'none'],cwd=foundations_contrib.root() / 'resources/model_serving/orbit')
        

    def test_retrieve_configuration_from_kubernetes(self):
        self._deploy()

        self.mock_ssh_file.write.assert_called_with(self.decoded_key)

    def test_setting_configuration_permissions(self):
        
        # self._setup_mocks_for_config_retrival()        
        mock_chmod = self.patch('os.chmod')

        self._deploy()
        
        mock_chmod.assert_called_with(self.ssh_key_path,  stat.S_IREAD)

    def test_removing_previous_configuration_if_exists(self):
        # self._setup_mocks_for_config_retrival()
        mock_path_exists = self.patch('os.path.exists', ConditionalReturn())
        mock_path_exists.return_when(True, self.ssh_key_path)

        mock_remove = self.patch('os.remove')

        self._deploy()

        mock_remove.assert_called_with(self.ssh_key_path)

    def test_not_removing_if_configuration_does_not_exists(self):
        mock_path_exists = self.patch('os.path.exists', ConditionalReturn())
        mock_path_exists.return_when(False, self.ssh_key_path)

        mock_remove = self.patch('os.remove')

        self._deploy()

        mock_remove.assert_not_called()

    def test_deploy_returns_true_if_run_process_successful(self):
        result = self._deploy()
        self.assertTrue(result)

    def test_deploy_returns_false_if_run_process_fails(self):
        self.mock_subprocess_object_for_deploy.returncode = 1

        result = self._deploy()
        self.assertFalse(result)

    def test_deploy_create_new_project_in_redis(self):
        
        self._deploy()
        self.mock_redis_execute_command.assert_called_once()

    def test_deploy_sends_information_to_redis_about_new_model_in_project(self):
        self._deploy()
        expected_results = { self.mock_model_name: pickle.dumps(self.model_information) }
        decoded_results = self._retrieve_results_from_redis(self.mock_project_name)
        
        self.assertEqual(expected_results, decoded_results)

    def test_deploy_sends_information_to_redis_for_multiple_models(self):
        self._deploy()
        self._deploy_second()

        decoded_results = self._retrieve_results_from_redis(self.mock_project_name)

        self.assertIsNotNone(decoded_results.get(self.mock_model_name))
        self.assertIsNotNone(decoded_results.get(self.mock_2nd_model_name))
        

    def test_deploy_upload_user_specified_model_directory(self):
        self._deploy()
        
        local_directory_key = '{}-{}'.format(self.mock_project_name, self.mock_model_name)
        directory_path = self.mock_project_directory
        local_job_id = '{}-{}'.format(self.mock_project_name, self.mock_model_name)

        self.mock_syncable_directories.assert_called_with(
            local_directory_key,
            directory_path,
            local_job_id,
            None,
            package_name='artifacts')


    def test_stop_returns_true_if_successful(self):
        result = self._stop()
        self.assertTrue(result)

    def test_stop_marks_model_as_deactivated(self):
        self._deploy()
        previous_status = self._get_model_status(self.mock_project_name, self.mock_model_name)
        self.assertEqual('activated', previous_status)

        self._stop()
        after_status = self._get_model_status(self.mock_project_name, self.mock_model_name)
        self.assertEqual('deactivated', after_status)

    def test_starting_previously_stopped_model_is_reactivated(self):
        self._deploy()
        self._stop()
        
        self._deploy()
        after_status = self._get_model_status(self.mock_project_name, self.mock_model_name)
        self.assertEqual('activated', after_status)

    def test_destroy_returns_true_if_successful(self):
        result = self._destroy()
        self.assertTrue(result)

    def test_destroy_removes_the_model_in_redis(self):
        self._deploy()
        self._destroy()

        decoded_results = self._retrieve_results_from_redis(self.mock_project_name)
        self.assertIsNone(decoded_results.get(self.mock_model_name))

    def test_model_first_is_set_to_default(self):
        self._deploy()
        model_status = self._get_model_default(self.mock_project_name, self.mock_model_name)
        self.assertEqual(True, model_status)

    def test_only_the_first_model_is_default(self):
        self._deploy()
        self._deploy_second()

        model_status = self._get_model_default(self.mock_project_name, self.mock_model_name)
        self.assertEqual(True, model_status)

        second_model_status = self._get_model_default(self.mock_project_name, self.mock_2nd_model_name)
        self.assertEqual(False, second_model_status)

    def test_created_at_for_model_is_set_correctly(self):
        self._deploy()
        model_created_at = self._get_model_param(self.mock_project_name, self.mock_model_name, 'created_at')
        self.assertEqual(self.mock_time(), model_created_at)

    def test_raise_value_error_exception_with_invalid_project_name(self):
        invalid_project_name = 'project-name'
        try:
            self._deploy(project_name=invalid_project_name)
            self.fail('Failed to test for expected behaviour')
        except ValueError as e:
            self.assertTrue('invalid project name' in str(e).lower())
        except Exception:
            self.fail('Invalid exception raised')
        
    def test_raise_value_error_exception_with_invalid_model_name(self):
        invalid_model_name = 'model-name'
        try:
            self._deploy(model_name=invalid_model_name)
            self.fail('Failed to test for expected behaviour')
        except ValueError as e:
            self.assertTrue('invalid model name' in str(e).lower())
        except Exception:
            self.fail('Invalid exception raised')

    def _deploy(self, project_name=None, model_name=None, project_directory=None):
        project_name = project_name if project_name is not None else self.mock_project_name
        model_name = model_name if model_name is not None else self.mock_model_name
        project_directory = project_directory if project_directory is not None else self.mock_project_directory

        from foundations_contrib.cli.orbit_model_package_server import deploy
        return deploy(project_name, model_name, project_directory)

    def _deploy_second(self):
        from foundations_contrib.cli.orbit_model_package_server import deploy
        return deploy(self.mock_project_name, self.mock_2nd_model_name, self.mock_project_directory)


    def _stop(self):
        from foundations_contrib.cli.orbit_model_package_server import stop
        return stop(self.mock_project_name, self.mock_model_name)

    def _destroy(self):
        from foundations_contrib.cli.orbit_model_package_server import destroy
        return destroy(self.mock_project_name, self.mock_model_name)

    def _get_model_param(self, project_name, model_name, param):
        import pickle
        decoded_results = self._retrieve_results_from_redis(project_name)
        model_details = decoded_results.get(model_name)
        deserialised_details = pickle.loads(model_details)
        return deserialised_details[param]

    def _get_model_status(self, project_name, model_name):
        return self._get_model_param(project_name, model_name, 'status')

    def _get_model_default(self, project_name, model_name):
        return self._get_model_param(project_name, model_name, 'default')

    def _retrieve_results_from_redis(self, project_name):
        hash_map_key = f'projects:{project_name}:model_listing'
        retrieved_results = self._redis.hgetall(hash_map_key)
        return {key.decode(): value for key, value in retrieved_results.items()}