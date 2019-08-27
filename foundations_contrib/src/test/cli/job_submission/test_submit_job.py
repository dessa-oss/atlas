"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.cli.job_submission.submit_job import submit

class TestJobSubmissionSubmit(Spec):
    
    mock_arguments = let_mock()
    mock_load_config = let_patch_mock('foundations_contrib.cli.job_submission.config.load')
    mock_stream_logs = let_patch_mock('foundations_contrib.cli.job_submission.logs.stream_job_logs')
    mock_deploy_deployment = let_patch_mock_with_conditional_return('foundations_contrib.cli.job_submission.deployment.deploy')
    mock_deployment = let_mock()
    mock_os_chdir = let_patch_mock('os.chdir')
    mock_os_getcwd = let_patch_mock('os.getcwd')

    mock_os_path_exists = let_patch_mock_with_conditional_return('os.path.exists')
    mock_open = let_patch_mock_with_conditional_return('builtins.open')

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return self.patch('foundations_contrib.global_state.config_manager', ConfigManager())

    @let
    def mock_file(self):
        mock = Mock()
        mock.__enter__ = lambda *args: mock
        mock.__exit__ = lambda *args: None
        mock.read.return_value = self.yaml_job_config
        return mock

    @let
    def job_config(self):
        return {
            'project_name': self.faker.name(),
            'log_level': self.faker.word(),
            'entrypoint': self.faker.uri_path(),
            'worker': self.faker.pydict(),
            'params': self.faker.pydict(),
        }

    @let
    def yaml_job_config(self):
        import yaml
        return yaml.dump(self.job_config)

    @let
    def scheduler_config(self):
        return self.faker.name()

    @let
    def current_directory(self):
        return self.faker.uri_path()
        
    @let
    def job_directory(self):
        return self.faker.uri_path()

    @let
    def project_name(self):
        return self.faker.sentence()

    @let
    def entrypoint(self):
        return self.faker.uri_path()

    @let
    def params(self):
        return self.faker.pydict()

    @set_up
    def set_up(self):
        self.mock_arguments.scheduler_config = None
        self.mock_arguments.job_dir = None
        self.mock_arguments.project_name = self.project_name
        self.mock_arguments.entrypoint = self.entrypoint
        self.mock_arguments.params = self.params
        
        self.mock_os_getcwd.return_value = self.current_directory
        self.mock_deploy_deployment.return_when(self.mock_deployment, self.project_name, self.entrypoint, self.params)
        self.mock_os_path_exists.return_when(False, 'job.config.yaml')

    def test_loads_default_scheduler_config(self):
        submit(self.mock_arguments)
        self.mock_load_config.assert_called_with('scheduler')

    def test_loads_specific_scheduler_config(self):
        self.mock_arguments.scheduler_config = self.scheduler_config
        submit(self.mock_arguments)
        self.mock_load_config.assert_called_with(self.scheduler_config)

    def test_runs_in_job_directory_when_specified(self):
        self.mock_arguments.job_dir = self.job_directory
        submit(self.mock_arguments)
        self.mock_os_chdir.assert_has_calls([call(self.job_directory), call(self.current_directory)])

    def test_runs_in_current_directory_when_no_job_dir_specified(self):
        submit(self.mock_arguments)
        self.mock_os_chdir.assert_has_calls([call(self.current_directory), call(self.current_directory)])

    def test_streams_log_from_created_deployment(self):
        submit(self.mock_arguments)
        self.mock_stream_logs.assert_called_with(self.mock_deployment)

    def test_does_not_break_when_interrupt_happens(self):
        self.mock_stream_logs.side_effect = self._send_interrupt
        with self.assert_does_not_raise():
            submit(self.mock_arguments)

    def test_sets_override_log_level_from_job_config(self):
        self._set_up_job_config()
        submit(self.mock_arguments)
        self.assertEqual(self.job_config['log_level'], self.config_manager['log_level'])

    def test_streams_log_from_deployment_using_override_config(self):
        self._set_up_job_config()
        submit(self.mock_arguments)
        self.mock_stream_logs.assert_called_with(self.mock_deployment)
        
    def _set_up_job_config(self):
        self.mock_deploy_deployment.clear()
        self.mock_deploy_deployment.return_when(
            self.mock_deployment, 
            self.job_config['project_name'], 
            self.job_config['entrypoint'], 
            self.job_config['params']
        )

        self.mock_os_path_exists.clear()
        self.mock_os_path_exists.return_when(True, 'job.config.yaml')
        self.mock_open.return_when(self.mock_file, 'job.config.yaml')

    def _send_interrupt(self, deployment):
        raise KeyboardInterrupt()