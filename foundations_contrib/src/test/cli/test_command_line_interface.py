"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import sys, os
import importlib
from mock import Mock, patch, call

from foundations_contrib.cli.command_line_interface import CommandLineInterface
from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
from foundations_production.serving.foundations_model_server import FoundationsModelServer
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

    @let_now
    def mock_environment(self):
        return self.patch('os.environ', {})

    @set_up
    def set_up(self):
        self._server_running = False
        self.psutil_process_mock.side_effect = self._process_constructor
        self.mock_environment['MODEL_SERVER_CONFIG_PATH'] = '/path/to/file'

    @patch('argparse.ArgumentParser')
    def test_correct_option_setup(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        level_1_subparsers_mock = Mock()
        parser_mock.add_subparsers.return_value = level_1_subparsers_mock

        level_2_parser_mock = Mock()
        level_1_subparsers_mock.add_parser.return_value = level_2_parser_mock

        level_2_subparsers_mock = Mock()
        level_2_parser_mock.add_subparsers.return_value = level_2_subparsers_mock

        level_3_parser_mock = Mock()
        level_2_subparsers_mock.add_parser.return_value = level_3_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')


        init_call = call('init', help='Creates a new Foundations project in the current directory')
        deploy_call = call('deploy', help='Deploys a Foundations project to the specified environment')
        info_call = call('info', help='Provides information about your Foundations project')
        serving_call = call('serving', help='Start serving a model package')

        level_1_subparsers_mock.add_parser.assert_has_calls([init_call, deploy_call, info_call, serving_call], any_order=True)

        init_argument_call = call('project_name', type=str, help='Name of the project to create')
        deploy_argument_file_call = call('driver_file', type=str, help='Name of file to deploy')
        deploy_argument_env_call = call('--env', help='Environment to run file in')
        info_argument_env_call = call('--env', action='store_true')

        level_2_parser_mock.add_argument.assert_has_calls(
            [
                init_argument_call,
                deploy_argument_env_call,
                deploy_argument_file_call,
                info_argument_env_call,
            ],
            any_order=True
        )

        serving_deploy_call = call('deploy', help='Deploy model package to foundations model package server')
        level_2_subparsers_mock.add_parser.assert_has_calls([serving_deploy_call], any_order=True)

        serving_deploy_rest_call = call('rest', help='Uses REST format content type')
        serving_deploy_domain_call = call('--domain', type=str, help='Domain and port of the model package server')
        serving_deploy_model_id_call = call('--model-id', type=str, help='Model package ID')
        serving_deploy_slug_call = call('--slug', type=str, help='Model package namespace string')

        level_3_parser_mock.add_argument.assert_has_calls(
            [
                serving_deploy_rest_call,
                serving_deploy_domain_call,
                serving_deploy_model_id_call,
                serving_deploy_slug_call,
            ]
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
        
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    def test_scaffold_creates_scaffold_with_project_name(self, scaffold_mock):
        CommandLineInterface(['init', 'my project']).execute()
        scaffold_mock.assert_called_with('my project')
        
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    def test_scaffold_creates_scaffold_with_project_name_different_project(self, scaffold_mock):
        CommandLineInterface(['init', 'my different project']).execute()
        scaffold_mock.assert_called_with('my different project')

    scaffold_project_mock = let_patch_mock('foundations_contrib.cli.scaffold.Scaffold.scaffold_project')
        
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

    def test_deploy_returns_correct_error_if_env_not_found(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=local']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `local`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_deploy_returns_correct_error_if_env_not_found_different_name(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `uat`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_exits_the_process_with_exit_status_of_one(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=non-existant-env']).execute()
        self.exit_mock.assert_called_with(1)

    def test_does_not_exit_when_environments_exist(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.exit_mock.assert_not_called()

    def test_deploy_returns_correct_error_if_wrong_directory(self):
        self.find_environment_mock.return_value = None
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Foundations project not found. Deploy command must be run in foundations project directory")
        self.exit_mock.assert_called_with(1)
     
    def test_deploys_job_when_local_config_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_not_called()

    config_manager = let_patch_mock('foundations.global_state.config_manager')
    sys_path = let_patch_mock('sys.path')
    run_file = let_patch_mock('importlib.import_module')

    @let
    def fake_model_server_pid(self):
        import random
        return random.randint(1,65000)

    @let_now
    def os_cwd(self):
        mock = self.patch('os.getcwd')
        mock.return_value = '/path/to/where/ever/we/are'
        return mock

    def _get_mock_file(self):
        mock_file_object = Mock()
        mock_file_object.__enter__ = lambda x: mock_file_object
        mock_file_object.__exit__ = Mock()
        return mock_file_object

    @let_now
    def mock_pid_file(self):
        return self._get_mock_file()

    @let_now
    def sleep_mock(self):
        return self.patch('time.sleep', self.MockSleep())

    @let
    def server_startup_time(self):
        from random import random

        between_zero_and_one = random()
        return between_zero_and_one * 0.7 + 0.2

    os_file_exists = let_patch_mock('os.path.isfile')
    os_chdir = let_patch_mock('os.chdir')
    os_kill = let_patch_mock('os.kill')
    subprocess_popen = let_patch_mock('subprocess.Popen')
    print_mock = let_patch_mock('builtins.print')
    exit_mock = let_patch_mock('sys.exit')
    open_mock = let_patch_mock('builtins.open')
    psutil_process_mock = let_patch_mock('psutil.Process')
    server_process = let_mock()
    requests_post_mock = let_patch_mock('requests.post')
    environment_fetcher_mock = let_patch_mock('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher.get_all_environments')
    find_environment_mock = let_patch_mock('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher.find_environment')

    def _process_constructor(self, pid):
        from psutil import NoSuchProcess

        if pid != self.fake_model_server_pid:
            raise AssertionError('process constructor needs to be called with model server pid {} (called with {})'.format(self.fake_model_server_pid, pid))

        if not self._server_running:
            raise NoSuchProcess(pid)

        return self.server_process

    def test_deploy_loads_config_when_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.config_manager.add_simple_config_path.assert_called_with("home/foundations/lou/config/uat.config.yaml")
    
    def test_deploy_adds_file_to_py_path(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/')
    
    def test_deploy_adds_file_to_py_path_different_path(self):
        self.os_cwd.return_value = 'home/foundations/hana/'
        self.find_environment_mock.return_value = ["home/foundations/hana/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/hana/')
    
    def test_deploy_returns_error_if_driver_file_does_not_exist(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = False
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.py', '--env=uat']).execute()
        self.os_file_exists.assert_called_with('home/foundations/lou/hana/driver.py')
        self.print_mock.assert_called_with('Driver file `hana/driver.py` does not exist')
        self.exit_mock.assert_called_with(1)
    
    def test_deploy_returns_error_if_driver_file_does_not_have_py_extension(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = True
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.exe', '--env=uat']).execute()
        self.print_mock.assert_called_with('Driver file `hana/driver.exe` needs to be a python file with an extension `.py`')
        self.exit_mock.assert_called_with(1)

    def test_deploy_imports_driver_file(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.run_file.assert_called_with('driver') 
    
    def test_deploy_imports_driver_file_different_file(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hippo/dingo.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/hippo')
        self.run_file.assert_called_with('dingo') 
    
    def test_deploy_imports_driver_file_different_name(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'passenger.py', '--env=uat']).execute()
        self.run_file.assert_called_with('passenger')

    def test_serving_deploy_rest_opens_pid_file(self):
        self._create_server_pidfile()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.open_mock.assert_any_call(FoundationsModelServer.pid_file_path, 'r')

    def test_serving_deploy_rest_reads_pid_file(self):
        self._create_server_pidfile()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.mock_pid_file.read.assert_called()

    def test_serving_deploy_rest_prints_message_if_web_server_is_already_running(self):
        self._bring_server_up()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_any_call('Model server is already running.')

    def test_serving_deploy_rest_runs_model_server_when_server_is_not_running(self):
        from subprocess import DEVNULL

        self._create_server_pidfile()
        self.server_process.cmdline.return_value = ['another_process.py']
        self._server_running = True
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=/path/to/file'], stdout=DEVNULL, stderr=DEVNULL)
                                              
    def test_serving_deploy_rest_starts_model_server_when_there_is_no_pidfile_and_process_not_running(self):
        from subprocess import DEVNULL

        self.open_mock.side_effect = OSError()

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=/path/to/file'], stdout=DEVNULL, stderr=DEVNULL)

    def test_serving_deploy_rest_starts_model_server_when_there_is_no_pidfile_and_process_not_running_different_model_config(self):
        from subprocess import DEVNULL

        self.open_mock.side_effect = OSError()
        self.mock_environment['MODEL_SERVER_CONFIG_PATH'] = 'a/path/to/another/file'

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=a/path/to/another/file'], stdout=DEVNULL, stderr=DEVNULL)

    def test_serving_deploy_rest_calls_prints_failure_message_if_server_fails_to_run(self):
        self.open_mock.side_effect = OSError()

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_any_call('Failed to start model server.', file=sys.stderr)
        self.exit_mock.assert_any_call(10)

    def test_serving_deploy_rest_calls_deploy_model_rest_api_if_server_is_running(self):
        self._bring_server_up()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        url = 'http://{}/v1/{}/'.format('localhost:8000', 'snail')
        self.requests_post_mock.assert_called_with(url, json = {'model_id':'some_id'})

    def test_serving_deploy_rest_informs_user_if_model_package_was_deployed_successfully(self):
        self._bring_server_up()
        response_mock = Mock()
        response_mock.status_code = 200
        self.requests_post_mock.return_value = response_mock
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_called_with('Model package was deployed successfully to model server.')

    def test_serving_deploy_rest_informs_user_if_model_package_failed_to_be_deployed(self):
        self._bring_server_up()
        response_mock = Mock()
        response_mock.status_code = 500
        self.requests_post_mock.return_value = response_mock
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_called_with('Failed to deploy model package to model server.', file=sys.stderr)
        self.exit_mock.assert_called_with(11)

    def test_serving_stop_kills_model_server(self):
        import signal

        self._bring_server_up()
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_called_once_with(self.fake_model_server_pid, signal.SIGINT)

    def test_serving_stop_does_not_kill_server_if_it_is_not_up(self):
        self.open_mock.side_effect = OSError()
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_not_called()

    def test_serving_stop_does_not_kill_process_if_it_is_model_server_process(self):
        self._create_server_pidfile()
        self.server_process.cmdline.return_value = ['another_process.py']
        self._server_running = True
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_not_called()

    def test_cli_does_not_fail_if_model_server_starts_before_900_ms(self):
        self.open_mock.side_effect = OSError()
        response_mock = Mock()
        response_mock.status_code = 200
        self.requests_post_mock.return_value = response_mock

        self.sleep_mock.time_to_wait = self.server_startup_time
        self.sleep_mock.callback = self._bring_server_up

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.exit_mock.assert_not_called()

    def _bring_server_up(self):
        self._create_server_pidfile()
        self._spawn_server_process()

    def _spawn_server_process(self):
        self.server_process.cmdline.return_value = ['foundations_production.serving.foundations_model_server']
        self._server_running = True

    def _create_server_pidfile(self):
        self.mock_pid_file.read.return_value = '{}'.format(self.fake_model_server_pid)
        self.open_mock = self.patch('builtins.open', ConditionalReturn())
        self.open_mock.return_when(self.mock_pid_file, FoundationsModelServer.pid_file_path, 'r')