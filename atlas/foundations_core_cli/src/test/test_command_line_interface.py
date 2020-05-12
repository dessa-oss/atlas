
from contextlib import contextmanager
import importlib
import sys, os
import unittest
from mock import Mock, patch, call, mock_open

from foundations_core_cli.command_line_interface import CommandLineInterface
from foundations_core_cli.environment_fetcher import EnvironmentFetcher
from foundations import ConfigManager

from foundations_spec import *

class TestCommandLineInterface(Spec):

    class MockSleep(object):

        _epsilon = 0.0001

        def __init__(self):
            self._time_elapsed = 0
            self.time_to_wait = 0
            self.callback = lambda: None

        def __call__(self, wait_time):
            self._time_elapsed += wait_time
            if self._time_elapsed >= self.time_to_wait - self._epsilon:
                self.callback()

    mock_subprocess_run = let_patch_mock('subprocess.run')
    psutil_process_mock = let_patch_mock('psutil.Process')
    current_foundations_context = let_patch_mock('foundations_contrib.global_state.current_foundations_context')
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')
    print_mock = let_patch_mock('builtins.print')
    environment_fetcher_mock = let_patch_mock('foundations_core_cli.environment_fetcher.EnvironmentFetcher.get_all_environments')
    mock_input = let_patch_mock('builtins.input')
    mock_getpass = let_patch_mock('getpass.getpass')
    mock_get = let_patch_mock('requests.get')
    mock_yaml_dump = let_patch_mock('yaml.dump')

    @let_now
    def mock_environment(self):
        return self.patch('os.environ', {})

    @let
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @let
    def level_1_subparsers_mock(self):
        return Mock()

    @let
    def level_2_subparsers_mock(self):
        return Mock()

    @let
    def level_2_parser_mock(self):
        return Mock()

    @let
    def level_3_parser_mock(self):
        return Mock()

    @let_now
    def mock_contrib_root(self):
        from pathlib import PosixPath

        path = self.faker.uri_path()
        return PosixPath(path)

    @let_now
    def current_foundations_context_instance(self):
        from foundations_internal.foundations_context import FoundationsContext

        foundations_context = FoundationsContext()
        self.current_foundations_context.return_value = foundations_context
        return foundations_context

    @let
    def command(self):
        return self.faker.sentence()

    @let
    def username(self):
        return self.faker.word()

    @let
    def password(self):
        return self.faker.word()

    @let
    def hostname(self):
        return self.faker.hostname()

    def fake_config_path(self, environment):
        return 'home/foundations/lou/config/{}.config.yaml'.format(environment)

    @set_up
    def set_up(self):
        self._server_running = False
        self.psutil_process_mock.side_effect = self._process_constructor
        self.mock_environment['MODEL_SERVER_CONFIG_PATH'] = '/path/to/file'
        self.patch('foundations_contrib.root', return_value=self.mock_contrib_root)

    def test_add_sub_parser_adds_new_subparser(self):
        hello_said = False

        cli = CommandLineInterface(['say_hello'])

        def _callback():
            hello_said = True
        parser = cli.add_sub_parser('say_hello')
        parser.set_defaults(function=_callback)
        cli.execute()

        self.assertTrue(True)

    @patch('argparse.ArgumentParser')
    def test_correct_option_setup(self, parser_class_mock):
        mock_str_to_bool = self.patch('foundations_core_cli.command_line_interface.CommandLineInterface._str_to_bool')

        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        parser_mock.add_subparsers.return_value = self.level_1_subparsers_mock

        self.level_1_subparsers_mock.add_parser.return_value = self.level_2_parser_mock
        self.level_2_parser_mock.add_subparsers.return_value = self.level_2_subparsers_mock

        self.level_2_subparsers_mock.add_parser.return_value = self.level_3_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')

        version_call = call('--version', action='store_true', help='Displays the current Foundations version')
        debug_call = call('--debug', action='store_true', help='Sets debug mode for the CLI')

        parser_mock.add_argument.assert_has_calls(
            [
                version_call,
                debug_call
            ]
        )

        init_call = call('init', help='Creates a new Foundations project in the current directory')
        info_call = call('info', help='Provides information about your Foundations project')

        self.level_1_subparsers_mock.add_parser.assert_has_calls(
            [
                init_call,
                info_call
            ],
            any_order=True
        )

        init_argument_call = call('project_name', type=str, help='Name of the project to create')
        info_argument_env_call = call('--env', action='store_true')

        self.level_2_parser_mock.add_argument.assert_has_calls(
            [
                init_argument_call,
                info_argument_env_call
            ],
            any_order=True
        )

    def test_execute_spits_out_help(self):
        with patch('argparse.ArgumentParser.print_help') as mock:
            CommandLineInterface([]).execute()
            mock.assert_called()

    @patch('foundations.__version__', '3.2.54')
    def test_execute_spits_out_version(self):
        CommandLineInterface(['--version']).execute()
        self.print_mock.assert_called_with('Running Foundations version 3.2.54')

    @patch('foundations.__version__', '7.3.3')
    def test_execute_spits_out_version_different_version(self):
        CommandLineInterface(['--version']).execute()
        self.print_mock.assert_called_with('Running Foundations version 7.3.3')

    @patch('foundations_core_cli.scaffold.Scaffold')
    def test_scaffold_creates_scaffold_with_project_name(self, scaffold_mock):
        CommandLineInterface(['init', 'my project']).execute()
        scaffold_mock.assert_called_with('my project') 

    @patch('foundations_core_cli.scaffold.Scaffold')
    def test_scaffold_creates_scaffold_with_project_name_different_project(self, scaffold_mock):
        CommandLineInterface(['init', 'my different project']).execute()
        scaffold_mock.assert_called_with('my different project')

    scaffold_project_mock = let_patch_mock('foundations_core_cli.scaffold.Scaffold.scaffold_project')

    def test_scaffold_scaffolds_with_project_name_different_project(self):
        CommandLineInterface(['init', 'my project']).execute()
        self.scaffold_project_mock.assert_called()

    def test_scaffold_prints_success_message(self):
        self.scaffold_project_mock.return_value = True

        CommandLineInterface(['init', 'my project']).execute()
        self.print_mock.assert_called_with('Success: New Foundations project `my project` created!')

    def test_scaffold_prints_success_message_different_project(self):
        self.scaffold_project_mock.return_value = True

        CommandLineInterface(['init', 'your project']).execute()
        self.print_mock.assert_called_with('Success: New Foundations project `your project` created!')

    def test_scaffold_prints_failure_message(self):
        self.scaffold_project_mock.return_value = False

        CommandLineInterface(['init', 'my project']).execute()
        self.print_mock.assert_called_with('Error: project directory for `my project` already exists')

    def test_scaffold_prints_failure_message_different_project(self):
        self.scaffold_project_mock.return_value = False

        CommandLineInterface(['init', 'your project']).execute()
        self.print_mock.assert_called_with('Error: project directory for `your project` already exists')

    def test_info_env_flag_returns_environment_none_available(self):
        self.environment_fetcher_mock.return_value = ([], [])
        CommandLineInterface(['info', '--env']).execute()
        self.print_mock.assert_called_with('No environments available')

    def test_info_env_flag_returns_environment_none_available_not_local(self):
        self.environment_fetcher_mock.return_value = (None, [])
        CommandLineInterface(['info', '--env']).execute()
        self.print_mock.assert_called_with('No environments available')

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_local(self, mock_print):
        self.environment_fetcher_mock.return_value = (['/home/local.config.yaml'], [])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with([['local','/home/local.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_local_different_environment(self, mock_print):
        self.environment_fetcher_mock.return_value = (['/home/config/uat.config.yaml'], [])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with([['uat','/home/config/uat.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_global(self, mock_print):
        self.environment_fetcher_mock.return_value = ([], ['/home/config/uat.config.yaml'])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with([['uat', '/home/config/uat.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_global_no_local(self, mock_print):
        self.environment_fetcher_mock.return_value = (None, ['/home/config/uat.config.yaml'])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_once()
        mock_print.assert_called_with([['uat', '/home/config/uat.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_local_and_global_available(self, mock_print):
        self.environment_fetcher_mock.return_value = (['/home/local.config.yaml'],['~/foundations/local.config.yaml'])
        CommandLineInterface(['info', '--env']).execute()
        project_call = call([['local', '/home/local.config.yaml']])
        global_call = call([['local','~/foundations/local.config.yaml']])
        mock_print.assert_has_calls([project_call, global_call], any_order = True)

    def test_login_without_username_password_args_prompts_user_for_info(self):
        CommandLineInterface(['login', f'{self.hostname}']).execute()
        self.mock_input.assert_called_once()
        self.mock_getpass.assert_called_once()

    def test_login_with_username_password_makes_token_request_basic_auth(self):
        CommandLineInterface(f'login {self.hostname} -u {self.username} -p {self.password}'.split()).execute()
        self.mock_get.assert_called_once_with(self.hostname + '/api/v2beta/auth/cli_login', auth=(self.username, self.password))

    def test_login_makes_token_request_using_basic_auth(self):
        self.mock_input.return_value = self.username
        self.mock_getpass.return_value = self.password
        CommandLineInterface(['login', f'{self.hostname}']).execute()
        self.mock_get.assert_called_once_with(self.hostname + '/api/v2beta/auth/cli_login', auth=(self.username, self.password))

    def test_login_writes_to_credentials_file_when_credentials_valid(self):
        access_token = self._set_up_mock_get_for_request(200)

        mock_file = self._execute_command_line_interface_in_patched_open(self.hostname)
        self.mock_yaml_dump.assert_called_with({'default': {'token': access_token}}, mock_file, default_flow_style=False)

    def test_login_prints_success_message_when_credentials_valid(self):
        self._set_up_mock_get_for_request(200)

        self._execute_command_line_interface_in_patched_open(self.hostname)
        self.print_mock.assert_called_with("\nLogin Succeeded!")

    def test_login_prints_failure_message_when_credentials_invalid(self):
        failure_message = self.faker.sentence()
        self._set_up_mock_get_for_request(400, text=failure_message)
        CommandLineInterface(['login', f'{self.hostname}']).execute()
        self.print_mock.assert_has_calls([call("\nLogin Failed!"), call(f"Error response: {failure_message}")])

    def _set_up_mock_get_for_request(self, status_code, text=''):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.text = text

        access_token = self.faker.word()
        mock_response.json.return_value = {'access_token': access_token}
        self.mock_get.return_value = mock_response

        return access_token

    def _execute_command_line_interface_in_patched_open(self, hostname):
        open_mock = mock_open()

        with patch('builtins.open', open_mock):
            mock_file = open_mock()
            try:
                CommandLineInterface(['login', f'{hostname}']).execute()
            finally:
                return mock_file

    def _process_constructor(self, pid):
        from psutil import NoSuchProcess

        if pid != self.fake_model_server_pid:
            raise AssertionError('process constructor needs to be called with model server pid {} (called with {})'.format(self.fake_model_server_pid, pid))

        if not self._server_running:
            raise NoSuchProcess(pid)

        return self.server_process