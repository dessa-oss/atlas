"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import pickle
from foundations_contrib.cli.orbit_model_package_server import deploy
from foundations_spec import *
import foundations_contrib


class TestOrbitModelPackageServer(Spec):
 
    mock_subprocess_run = let_patch_mock('subprocess.run')
    mock_syncable_directories = let_patch_mock('foundations.artifacts.syncable_directory.SyncableDirectory')
    mock_foundations_set_environment = let_patch_mock('foundations.set_environment')

    @let
    def mock_project_name(self):
        return self.faker.word()

    @let
    def mock_model_name(self):
        return self.faker.word()

    @let
    def mock_project_directory(self):
        return self.faker.uri_path()

    @let
    def model_information(self):
        return {
            'status': 'activated',
            'default': False,
            'created_by': '',
            'created_at': '',
            'description': '',
            'entrypoints': {},
            'validation_metrics': {}
        }

    @set_up
    def set_up(self):
        self.maxDiff=None
        import fakeredis
        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    def test_deploy_run_deployment_script_with_project_name_model_name_project_directory(self):
        result = deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)

        self.mock_foundations_set_environment.assert_called_with('local')

        self.mock_subprocess_run.assert_called_with([
            'bash',
            './deploy_serving.sh',
            self.mock_project_name,
            self.mock_model_name],
            cwd=foundations_contrib.root() / 'resources/model_serving/orbit')

        self.assertTrue(result)

    def test_deploy_returns_false_if_model_exists_in_project(self):
        first_result = deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)
        self.assertTrue(first_result)

        second_result = deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)
        self.assertFalse(second_result)

    def test_deploy_sends_information_to_redis_about_new_model_in_project(self):
        result = deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)
        self.assertTrue(result)

        expected_results = { self.mock_model_name: pickle.dumps(self.model_information) }

        hash_map_key = f'projects:{self.mock_project_name}:model_listing'
        retrieved_results = self._redis.hgetall(hash_map_key)
        decoded_results = {key.decode(): value for key, value in retrieved_results.items()}

        self.assertEqual(expected_results, decoded_results)

    def test_deploy_upload_user_specified_model_directory(self):
        deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)
        
        local_directory_key = '{}-{}'.format(self.mock_project_name, self.mock_model_name)
        directory_path = self.mock_project_directory
        local_job_id = '{}-{}'.format(self.mock_project_name, self.mock_model_name)

        self.mock_syncable_directories.assert_called_with(
            local_directory_key,
            directory_path,
            local_job_id,
            None)
