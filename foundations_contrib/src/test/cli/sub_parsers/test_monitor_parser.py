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

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

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
        cmd = 'monitor pause {self.monitor_name} {self.project_name}'
        CommandLineInterface(cmd.split()).execute()
        mock_method.assert_called_once()

    def test_monitor_calls_cron_job_scheduler_for_pausing_with_parameters_passed_by_cli(self):
        mock_config_manager = self.patch('foundations_contrib.foundations_contrib.global_state.config_manager')
        mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000'}

        cmd = f'monitor pause {self.monitor_name} {self.project_name}' 
        CommandLineInterface(cmd.split()).execute()
        self.cron_job_scheduler.pause_job.assert_called_once_with(self.monitor_package_id)
