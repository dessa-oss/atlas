"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_core_cli.command_line_interface import CommandLineInterface
from foundations_orbit_cli.sub_parsers.monitor.monitor_parser import MonitorParser
from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError

class TestMonitorParser(Spec):

    @set_up
    def set_up(self):
        mock_config_manager = self.patch('foundations_contrib.foundations_contrib.global_state.config_manager')
        mock_config_manager.config.return_value = {'scheduler_url': self.scheduler_url}
        self.mock_print = self.patch('builtins.print')
        self.patch('foundations_core_cli.job_submission.config.load')

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
    def job_directory(self):
        return self.faker.word()

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let
    def invalid_operation(self):
        return self.faker.word()

    @let
    def scheduler_url(self):
        return self.faker.url()

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
        mock_add_parser = self.patch('foundations_orbit_cli.sub_parsers.monitor.monitor_parser.MonitorParser.add_sub_parser')
        CommandLineInterface([''])
        mock_add_parser.assert_called_once()

    def test_sub_parser_called_specifically_for_monitor(self):
        mock_argument_parser = self.patch('foundations_core_cli.command_line_interface.CommandLineInterface.add_sub_parser')
        CommandLineInterface([''])
        help_msg = 'Provides operations for managing monitors in Orbit'
        mock_argument_parser.assert_any_call('monitor', help=help_msg)

    def test_monitor_calls_start_method_when_create_command_is_triggered(self):
        mock_method = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self._call_monitor_command('create')
        mock_method.assert_called_once()

    def test_monitor_calls_pause_monitor_when_pause_command_is_triggered(self):
        mock_method = self.patch('foundations_orbit_cli.sub_parsers.monitor.monitor_parser.MonitorParser._pause_monitor')
        self._call_monitor_command('pause')
        mock_method.assert_called_once()

    def test_monitor_calls_cron_job_scheduler_for_pausing_with_parameters_passed_by_cli(self):
        self._call_monitor_command('pause')
        self.cron_job_scheduler.pause_job.assert_called_once_with(self.monitor_package_id)

    def test_monitor_prints_success_message_when_pause_executes_successfully(self):
        self._call_monitor_command('pause')
        self.mock_print.assert_called_with(f'Successfully paused monitor {self.monitor_name} from project {self.project_name}')
    
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
        mock_monitor_delete = self.patch('foundations_core_cli.orbit_monitor_package_server.delete')
        mock_monitor_delete.__name__ = 'delete'
        self._call_monitor_command('delete')
        mock_monitor_delete.assert_called_with(self.project_name, self.monitor_name, 'scheduler')

    def test_monitor_delete_exits_non_zero_status_when_cron_job_scheduler_fails_to_delete(self):
        error_message = f'Deleting failed'
        mock_exit = self.patch('sys.exit')
        self.cron_job_scheduler.delete_job.side_effect = CronJobSchedulerError(error_message)
        self._call_monitor_command('delete')
        mock_exit.assert_called_once_with(f'Command failed with error: {error_message}')

    def test_monitor_prints_success_message_when_delete_executes_successfully(self):
        mock_monitor_delete = self.patch('foundations_core_cli.orbit_monitor_package_server.delete')
        mock_monitor_delete.__name__ = 'delete'
        self._call_monitor_command('delete')
        self.mock_print.assert_called_with(f'Successfully deleted monitor {self.monitor_name} from project {self.project_name}')

    def test_monitor_calls_resume_monitor_when_resume_command_is_triggered(self):
        mock_method = self.patch('foundations_orbit_cli.sub_parsers.monitor.monitor_parser.MonitorParser._resume_monitor')
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

    def test_monitor_prints_success_message_when_resume_executes_successfully(self):
        self._call_monitor_command('resume')
        self.mock_print.assert_called_with(f'Successfully resumed monitor {self.monitor_name} from project {self.project_name}')

    def test_monitor_calls_pause_sends_project_name_model_name_and_env_to_monitor_package_server(self):
        mock_pause = self.patch('foundations_core_cli.orbit_monitor_package_server.pause')
        mock_pause.__name__ = 'pause'
        self._call_monitor_command('pause')
        mock_pause.assert_called_once_with(self.project_name, self.monitor_name, self.env)

    def test_monitor_calls_resume_sends_project_name_model_name_and_env_to_monitor_package_server(self):
        mock_resume = self.patch('foundations_core_cli.orbit_monitor_package_server.resume')
        mock_resume.__name__ = 'resume'
        self._call_monitor_command('resume')
        mock_resume.assert_called_once_with(self.project_name, self.monitor_name, self.env)

    def test_monitor_prints_failure_message_when_start_raises_value_error(self):
        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self.patch('sys.exit')
        mock_monitor_start.side_effect = ValueError('Creating failed')
        command = f'monitor create --project_name={self.project_name} --name={self.monitor_name} --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        self.mock_print.assert_called_with(f'Unable to create monitor {self.monitor_name} in project {self.project_name}')

    def test_monitor_prints_failure_message_when_start_raises_value_error_when_name_and_project_name_not_set(self):
        mock_getcwd = self.patch('os.getcwd')
        mock_getcwd.return_value = self.job_directory
        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self.patch('sys.exit')
        mock_monitor_start.side_effect = ValueError('Creating failed')

        command = f'monitor create --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        self.mock_print.assert_called_with(f'Unable to create monitor main-py in project {self.job_directory}')

    def test_monitor_returns_exit_non_zero_when_start_raises_value_error(self):
        error_message_thrown = 'Creating failed'
        mock_system_exit = self.patch('sys.exit')
        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')

        mock_monitor_start.side_effect = ValueError(error_message_thrown)
        command = f'monitor create --project_name={self.project_name} --name={self.monitor_name} --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        mock_system_exit.assert_called_once_with(f'Command failed with error: {error_message_thrown}')

    def test_create_monitor_prints_failure_message_when_start_raises_connection_error(self):
        from requests.exceptions import ConnectionError

        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self.patch('sys.exit')
        mock_monitor_start.side_effect = ConnectionError
        command = f'monitor create --project_name={self.project_name} --name={self.monitor_name} --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        self.mock_print.assert_called_with(f'Unable to create monitor {self.monitor_name} in project {self.project_name}')

    def test_monitor_prints_failure_message_when_start_raises_connection_error_when_project_name_and_directory_not_set(self):
        from requests.exceptions import ConnectionError

        mock_getcwd = self.patch('os.getcwd')
        mock_getcwd.return_value = self.job_directory
        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self.patch('sys.exit')
        mock_monitor_start.side_effect = ConnectionError

        command = f'monitor create --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        self.mock_print.assert_called_with(f'Unable to create monitor main-py in project {self.job_directory}')

    def test_monitor_returns_exit_non_zero_when_start_raises_connection_error(self):
        from requests.exceptions import ConnectionError

        error_message_thrown = f'Could not connect to scheduler at {self.scheduler_url}'
        mock_system_exit = self.patch('sys.exit')
        mock_monitor_start = self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        mock_monitor_start.side_effect = ConnectionError

        command = f'monitor create --project_name={self.project_name} --name={self.monitor_name} --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()
        mock_system_exit.assert_called_once_with(f'Command failed with error: {error_message_thrown}')

    def test_monitor_prints_success_message_when_created_successfully(self):
        self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self._call_monitor_command('resume')

        command = f'monitor create --project_name={self.project_name} --name={self.monitor_name} --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()

        self.mock_print.assert_called_with(f'Successfully created monitor {self.monitor_name} in project {self.project_name}')

    def test_monitor_prints_success_message_when_created_successfully_without_project_name_or_monitor_name_specified(self):
        mock_getcwd = self.patch('os.getcwd')
        mock_getcwd.return_value = self.job_directory
        self.patch('foundations_core_cli.orbit_monitor_package_server.start')
        self._call_monitor_command('resume')

        command = f'monitor create --env={self.env} . main.py'
        CommandLineInterface(command.split()).execute()

        self.mock_print.assert_called_with(f'Successfully created monitor main-py in project {self.job_directory}')

    def test_delete_monitor_prints_failure_message_when_delete_raises_connection_error(self):
        self._test_command_prints_failure_message_with_connection_error('delete')

    def test_monitor_returns_exit_non_zero_when_delete_raises_connection_error(self):
        self._test_command_exits_with_connection_error('delete')

    def test_pause_monitor_prints_failure_message_when_pause_raises_connection_error(self):
        self._test_command_prints_failure_message_with_connection_error('pause')

    def test_monitor_returns_exit_non_zero_when_pause_raises_connection_error(self):
        self._test_command_exits_with_connection_error('pause')

    def test_resume_monitor_prints_failure_message_when_resume_raises_connection_error(self):
        self._test_command_prints_failure_message_with_connection_error('resume')

    def test_monitor_returns_exit_non_zero_when_resume_raises_connection_error(self):
        self._test_command_exits_with_connection_error('resume')

    def test_monitor_returns_exit_non_zero_when_resume_raises_connection_error_when_no_url_set(self):
        self._test_command_exits_with_connection_error_when_no_scheduler_url_in_config('resume')
    
    def test_monitor_returns_exit_non_zero_when_pause_raises_connection_error_when_no_url_set(self):
        self._test_command_exits_with_connection_error_when_no_scheduler_url_in_config('pause')

    def test_monitor_returns_exit_non_zero_when_delete_raises_connection_error_when_no_url_set(self):
        self._test_command_exits_with_connection_error_when_no_scheduler_url_in_config('delete')

    def _test_command_exits_with_connection_error_when_no_scheduler_url_in_config(self, command):
        mock_config_manager = self.patch('foundations_contrib.global_state.config_manager')
        mock_config_manager.config.return_value = {}
        self._test_command_exits_with_connection_error(command, url='http://localhost:5000')

    def _test_command_exits_with_connection_error(self, command, url=None):
        url = url if url is not None else self.scheduler_url
        error_message = f'Could not connect to scheduler at {url}'
        mock_system_exit = self.patch('sys.exit')
        self._patch_monitor_command_with_connection_error(command)
        mock_system_exit.assert_called_with(f'Command failed with error: {error_message}')

    def _test_command_prints_failure_message_with_connection_error(self, command):
        self.patch('sys.exit')
        self._patch_monitor_command_with_connection_error(command)
        self.mock_print.assert_called_with(f'Unable to {command} monitor {self.monitor_name} from project {self.project_name}')

    def _patch_monitor_command_with_connection_error(self, command):
        from requests.exceptions import ConnectionError

        mock = self.patch(f'foundations_core_cli.orbit_monitor_package_server.{command}')
        mock.__name__ = command
        mock.side_effect = ConnectionError
        self._call_monitor_command(command)

    def test_invalid_option_for_monitor_command(self):
        try:
            CommandLineInterface(f'monitor {self.invalid_operation}'.split()).execute()
            self.fail('Failed to fail for invalid monitor operations')
        except SystemExit as e:
            self.assertTrue(e != 0)

    def _call_monitor_command(self, command):
        cmd = f'monitor {command} {self.project_name} {self.monitor_name} --env={self.env}'
        CommandLineInterface(cmd.split()).execute()
