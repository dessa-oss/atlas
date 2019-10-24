"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_contrib.cli.command_line_interface import CommandLineInterface
from foundations_contrib.cli.sub_parsers.monitor_parser import MonitorParser
from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError

class TestMonitorParser(Spec):

    @set_up
    def set_up(self):
        mock_config_manager = self.patch('foundations_contrib.foundations_contrib.global_state.config_manager')
        mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000'}
        self.patch('foundations_contrib.cli.job_submission.config.load')

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def env(self):
        return 'scheduler'

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let
    def invalid_operation(self):
        return self.faker.word()

    @let_now
    def cron_job_scheduler(self):
        mock_cron_job_scheduler = Mock()
        mock_cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
        mock_cron_job_scheduler_class.return_value = mock_cron_job_scheduler
        return mock_cron_job_scheduler

    def test_sub_parser_retrieves_command_line_interface_as_a_parameter(self):
        cli = CommandLineInterface([''])
        sub_parser = MonitorParser(cli)
        self.assertTrue(type(sub_parser._cli) is CommandLineInterface)

    def test_sub_parser_setup_parser_on_cli_instantiation(self):
        mock_add_parser = self.patch('foundations_contrib.cli.sub_parsers.monitor_parser.MonitorParser.add_sub_parser')
        CommandLineInterface([''])
        mock_add_parser.assert_called_once()

    def test_sub_parser_called_specifically_for_monitor(self):
        mock_argument_parser = self.patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.add_sub_parser')
        CommandLineInterface([''])
        help_msg = 'Provides operations for managing monitors in Orbit'
        mock_argument_parser.assert_any_call('monitor', help=help_msg)

    def test_monitor_calls_pause_monitor_when_pause_command_is_triggered(self):
        mock_method = self.patch('foundations_contrib.cli.sub_parsers.monitor_parser.MonitorParser._pause_monitor')
        self._call_monitor_command('pause')
        mock_method.assert_called_once()

    def test_monitor_calls_cron_job_scheduler_for_pausing_with_parameters_passed_by_cli(self):
        self._call_monitor_command('pause')
        self.cron_job_scheduler.pause_job.assert_called_once_with(self.monitor_package_id)
    
    def test_monitor_returns_exit_non_zero_when_cron_job_scheduler_fails_to_pause(self):
        error_message_thrown = 'Pausing failed'
        mock_system_exit = self.patch('sys.exit')
        self.cron_job_scheduler.pause_job.side_effect = CronJobSchedulerError(error_message_thrown)
        self._call_monitor_command('pause')
        mock_system_exit.assert_called_once_with(f'Command failed with error: {error_message_thrown}')

    def _call_pause_monitor_command(self, command):
        cmd = f'monitor {command} {self.monitor_name} {self.project_name}'
        CommandLineInterface(cmd.split()).execute()

    def test_monitor_delete_with_specified_monitor_name_and_project_name_calls_delete(self):
        mock_monitor_delete = self.patch('foundations_contrib.cli.orbit_monitor_package_server.delete')
        self._call_monitor_command('delete')
        mock_monitor_delete.assert_called_with(self.project_name, self.monitor_name, 'scheduler')

    def test_monitor_delete_exits_non_zero_status_when_cron_job_scheduler_fails_to_delete(self):
        error_message = f'Deleting failed'
        mock_exit = self.patch('sys.exit')
        self.cron_job_scheduler.delete_job.side_effect = CronJobSchedulerError(error_message)
        self._call_monitor_command('delete')
        mock_exit.assert_called_once_with(f'Command failed with error: {error_message}')

    def test_monitor_calls_resume_monitor_when_resume_command_is_triggered(self):
        mock_method = self.patch('foundations_contrib.cli.sub_parsers.monitor_parser.MonitorParser._resume_monitor')
        self._call_monitor_command('resume')
        mock_method.assert_called_once()

    def test_monitor_calls_cron_job_scheduler_for_resuming_with_parameters_passed_by_cli(self):
        self._call_monitor_command('resume')
        self.cron_job_scheduler.resume_job.assert_called_once_with(self.monitor_package_id)
    
    def test_monitor_returns_exit_non_zero_when_cron_job_scheduler_fails_to_resume(self):
        error_message_thrown = 'Resuming failed'
        mock_system_exit = self.patch('sys.exit')
        self.cron_job_scheduler.resume_job.side_effect = CronJobSchedulerError(error_message_thrown)
        self._call_monitor_command('resume')
        mock_system_exit.assert_called_once_with(f'Command failed with error: {error_message_thrown}')

    def test_monitor_calls_pause_sends_project_name_model_name_and_env_to_monitor_package_server(self):
        mock_pause = self.patch('foundations_contrib.cli.orbit_monitor_package_server.pause')
        self._call_monitor_command('pause')
        mock_pause.assert_called_once_with(self.project_name, self.monitor_name, self.env)

    def test_monitor_calls_resume_sends_project_name_model_name_and_env_to_monitor_package_server(self):
        mock_resume = self.patch('foundations_contrib.cli.orbit_monitor_package_server.resume')
        self._call_monitor_command('resume')
        mock_resume.assert_called_once_with(self.project_name, self.monitor_name, self.env)

    def test_invalid_option_for_monitor_command(self):
        try:
            CommandLineInterface(f'monitor {self.invalid_operation}'.split()).execute()
            self.fail('Failed to fail for invalid monitor operations')
        except SystemExit as e:
            self.assertTrue(e != 0)

    def _call_monitor_command(self, command):
        cmd = f'monitor {command} {self.project_name} {self.monitor_name} --env={self.env}'
        CommandLineInterface(cmd.split()).execute()
