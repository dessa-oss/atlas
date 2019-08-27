"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_spec.extensions import let_fake_redis

from foundations_contrib.config_manager import ConfigManager
from foundations.deploy import deploy

class TestDeploy(Spec):

    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')

    config_manager = let_patch_mock('foundations.config_manager', ConfigManager())
    mock_yaml_load = let_patch_mock('yaml.load', ConditionalReturn())
    mock_json_dump = let_patch_mock('json.dump')

    mock_set_environment = let_patch_mock('foundations.set_environment')

    mock_redis = let_fake_redis()

    @let_now
    def fake_cwd(self):
        cwd_path = self.faker.file_path()
        patched_os_getcwd = self.patch('os.getcwd')
        patched_os_getcwd.return_value = cwd_path
        return cwd_path

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def environment(self):
        return self.faker.word()

    @let
    def entrypoint(self):
        return self.faker.file_path()

    @let
    def job_directory(self):
        return self.faker.file_path()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def params(self):
        return {
            "learning_rate": 0.125,
            "layers": [
                {
                    "neurons": 5
                },
                {
                    "neurons": 6
                }
            ]
        }

    @let
    def deployment_wrapper(self):
        from foundations_contrib.deployment_wrapper import DeploymentWrapper

        deployment = Mock()
        deployment.job_name.return_value = self.job_id

        return DeploymentWrapper(deployment)

    @set_up
    def set_up(self):
        import os.path as path
        from foundations_contrib.global_state import current_foundations_context
        self._old_project_name = current_foundations_context().project_name()

        config = {
            'job_deployment_env': 'local',
            'results_config': {},
            'cache_config': {}
        }

        self.patch('foundations_contrib.global_state.redis_connection', self.mock_redis)

        self.mock_open = self.patch('builtins.open', ConditionalReturn())

        self.mock_file = Mock()
        self.mock_params_file = Mock()

        self.mock_yaml_load.return_when(config, self.mock_file)

        self.mock_file.__enter__ = lambda *args: self.mock_file
        self.mock_file.__exit__ = lambda *args: None

        self.mock_params_file.__enter__ = lambda *args: self.mock_params_file
        self.mock_params_file.__exit__ = lambda *args: None

        self.mock_open.return_when(self.mock_file, '~/.foundations/config/local.config.yaml', 'r')
        self.mock_open.return_when(self.mock_file, '~/.foundations/config/{}.config.yaml'.format(self.environment), 'r')
        self.mock_open.return_when(self.mock_params_file, 'foundations_job_parameters.json', 'w')

        log_file_path = path.expanduser('~/.foundations/logs/system.log')
        self.mock_open.return_when(self.mock_file, log_file_path, 'a', encoding=None)

        self.mock_set_environment.side_effect = self._set_environment

        self.mock_deploy_job_function = self.patch('foundations.job_deployer.deploy_job')
        self.mock_deploy_job_function.return_value = self.deployment_wrapper

        self.pipeline_context = current_foundations_context().pipeline_context()

        self.mock_chdir = self.patch('os.chdir', self._mock_chdir)
        self._directory_stack = []

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import current_foundations_context
        current_foundations_context().set_project_name(self._old_project_name)

    def test_redis_not_used_before_environment_set(self):
        self._environment_set = False

        def _break_redis_if_no_environment_set(*args):
            if not self._environment_set:
                raise AssertionError('Environment not set')

        def _set_environment(*args):
            self._environment_set = True

        self.mock_redis.incr = _break_redis_if_no_environment_set
        self.mock_set_environment.side_effect = _set_environment

        deploy(self.project_name, self.environment, self.entrypoint, self.job_directory, self.params)

    def test_deploy_logs_that_we_deployed_via_the_sdk(self):
        deploy(self.project_name, self.environment, self.entrypoint, self.job_directory, self.params)
        message = {
            'project_name': self.project_name, 
            'environment': self.environment, 
            'entrypoint': self.entrypoint, 
            'job_directory': self.job_directory, 
            'params': self.params
        }
        self.mock_message_router.push_message.assert_called_with('job_deployed_with_sdk', message)


    def test_deploy_with_defaults_sets_project_name_to_cwd_basename(self):
        import os.path as path

        cwd_name = path.basename(self.fake_cwd)
        self._test_deploy_correctly_sets_project_name(cwd_name)

    def test_deploy_with_project_name_specified_sets_project_name_to_specified_project_name(self):
        self._test_deploy_correctly_sets_project_name(self.project_name, project_name=self.project_name)

    def test_deploy_with_defaults_sets_environment_to_local(self):
        deploy()
        self.mock_set_environment.assert_called_with('local')

    def test_deploy_adds_path_for_specified_config(self):
        deploy(env=self.environment)
        self.mock_set_environment.assert_called_with(self.environment)

    def test_deploy_with_defaults_deploys_job_with_entrypoint_set_to_main_py(self):
        deploy()
        self.assertEqual('main.py', self.config_manager['run_script_environment']['script_to_run'])

    def test_deploy_with_entrypoint_set_deploys_job_with_entrypoint_set(self):
        deploy(entrypoint=self.entrypoint)
        self.assertEqual(self.entrypoint, self.config_manager['run_script_environment']['script_to_run'])

    def test_deploy_with_defaults_deploys_job(self):
        mock_pipeline_context_wrapper = Mock()
        mock_pipeline_context_wrapper.pipeline_context.return_value = self.pipeline_context
        mock_pipeline_context_wrapper_klass = self.patch('foundations_internal.pipeline_context_wrapper.PipelineContextWrapper', ConditionalReturn())
        mock_pipeline_context_wrapper_klass.return_when(mock_pipeline_context_wrapper, self.pipeline_context)

        deploy()
        self.mock_deploy_job_function.assert_called_once_with(mock_pipeline_context_wrapper, None, {})

    def test_deploy_sets_enable_stages_to_false(self):
        deploy()
        self.assertFalse(self.config_manager['run_script_environment']['enable_stages'])

    def test_deploy_with_job_directory_set_deploys_from_that_directory(self):
        deploy(job_directory=self.job_directory)
        self.assertIn(self.job_directory, self._directory_stack)

    def test_deploy_with_job_directory_set_changes_directory_back_after_deployment(self):
        deploy(job_directory=self.job_directory)
        self.assertEqual([self.job_directory, self.fake_cwd], self._directory_stack)

    def test_deploy_with_defaults_does_not_chdir_to_any_directory(self):
        deploy()
        self.assertEqual([], self._directory_stack)

    def test_deploy_with_project_name_not_set_but_with_job_directory_set_correctly_sets_project_name(self):
        import os.path as path

        project_name = path.basename(self.job_directory)
        self._test_deploy_correctly_sets_project_name(project_name, job_directory=self.job_directory)

    def test_deploy_with_parameters_set_but_job_directory_not_set_writes_parameters_file_to_cwd(self):
        deploy(params=self.params)
        self.mock_json_dump.assert_called_with(self.params, self.mock_params_file)

    def test_deploy_with_defaults_does_not_write_any_params_file(self):
        deploy()
        self.mock_open.assert_called_once_with('~/.foundations/config/local.config.yaml', 'r')

    def test_deploy_available_from_foundations_module(self):
        import foundations
        self.assertEqual(deploy, foundations.deploy)

    def test_deploy_returns_deployment_wrapper_which_has_job_id(self):
        deployment_wrapper = deploy()
        self.assertEqual(self.job_id, deployment_wrapper.job_name())

    def test_deploy_returns_deployment_wrapper_object(self):
        from foundations_contrib.deployment_wrapper import DeploymentWrapper

        deployment_wrapper = deploy()
        self.assertIsInstance(deployment_wrapper, DeploymentWrapper)

    def test_counts_deploy_amount(self):
        from foundations_contrib.deployment_wrapper import DeploymentWrapper

        deploy()
        self.assertEqual('1', self.mock_redis.get('foundations:sdk:deloyment_count').decode())

    def _test_deploy_correctly_sets_project_name(self, expected_project_name, **kwargs):
        from foundations_contrib.global_state import current_foundations_context

        deploy(**kwargs)
        self.assertEqual(expected_project_name, current_foundations_context().project_name())

    def _set_environment(self, environment_name):
        from foundations_contrib.global_state import config_manager

        path = '~/.foundations/config/{}.config.yaml'.format(environment_name)
        config_manager.add_simple_config_path(path)

    def _mock_chdir(self, directory):
        self._directory_stack.append(directory)