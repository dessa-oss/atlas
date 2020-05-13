
from foundations_spec import *

from foundations_core_cli.job_submission.deployment import deploy

class TestJobSubmissionDeployment(Spec):

    mock_os_getcwd = let_patch_mock('os.getcwd')
    mock_deploy_job = let_patch_mock_with_conditional_return('foundations_contrib.job_deployer.deploy_job')
    mock_deployment = let_mock()
    mock_json_dump = let_patch_mock('json.dump')

    @let
    def project_name(self):
        return self.faker.sentence()

    @let
    def current_directory(self):
        return f'{self.faker.uri_path()}/{self.project_name}'

    @let_now
    def foundations_job(self):
        from foundations_internal.foundations_job import FoundationsJob
        return self.patch('foundations_contrib.global_state.foundations_job', FoundationsJob())

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return self.patch('foundations_contrib.global_state.config_manager', ConfigManager())

    @let
    def entrypoint(self):
        return self.faker.uri_path()

    @let
    def params(self):
        return {key: self.faker.sentence() for key in self.faker.words()}

    mock_open = let_patch_mock_with_conditional_return('builtins.open')

    @let
    def mock_file(self):
        mock = Mock()
        mock.__enter__ = lambda *args: mock
        mock.__exit__ = lambda *args: None
        return mock

    mock_context_wrapper = let_mock()
    mock_get_user_name_from_token = let_patch_mock('foundations_core_cli.job_submission.deployment._get_user_name_from_token')

    @set_up
    def set_up(self):
        self.mock_os_getcwd.return_value = self.current_directory
        self.mock_open.return_when(self.mock_file, 'foundations_job_parameters.json', 'w+')
        self.mock_deploy_job.return_when(self.mock_deployment, self.foundations_job, None, {})

    def test_sets_project_name_from_parameter(self):
        deploy(self.project_name, self.entrypoint, self.params)
        self.assertEqual(self.project_name, self.foundations_job.project_name)

    def test_sets_project_name_from_current_directory_when_not_specified(self):
        deploy(None, self.entrypoint, self.params)
        self.assertEqual(self.project_name, self.foundations_job.project_name)

    def test_sets_run_script_environment_to_include_entrypoint(self):
        deploy(self.project_name, self.entrypoint, self.params)
        self.assertEqual({'script_to_run': self.entrypoint, 'enable_stages': False}, self.config_manager['run_script_environment'])

    def test_defaults_entrypoint_to_none(self):
        deploy(self.project_name, None, self.params)
        self.assertEqual({'script_to_run': None, 'enable_stages': False}, self.config_manager['run_script_environment'])

    def test_writes_params_as_json_to_file(self):
        import json

        deploy(self.project_name, self.entrypoint, self.params)
        self.mock_json_dump.assert_called_with(self.params, self.mock_file)

    def test_deploy_returns_created_deployment(self):
        deployment = deploy(self.project_name, self.entrypoint, self.params)
        self.assertEqual(self.mock_deployment, deployment)