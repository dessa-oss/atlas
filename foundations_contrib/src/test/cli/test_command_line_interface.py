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
from foundations import ConfigManager


from foundations_internal.testing.helpers import let, let_now, let_patch_mock
from foundations_internal.testing.helpers.spec import Spec


class TestCommandLineInterface(Spec):

    @patch('argparse.ArgumentParser')
    def test_correct_option_setup(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        sub_parsers_mock = Mock()
        parser_mock.add_subparsers.return_value = sub_parsers_mock

        specific_parser_mock = Mock()
        sub_parsers_mock.add_parser.return_value = specific_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')


        init_call = call('init', help='Creates a new Foundations project in the current directory')
        deploy_call = call('deploy', help='Deploys a Foundations project to the specified environment')
        info_call = call('info', help='Provides information about your Foundations project')

        sub_parsers_mock.add_parser.assert_has_calls([init_call, deploy_call, info_call], any_order=True)

        init_argument_call = call('project_name', type=str, help='Name of the project to create')
        deploy_argument_file_call = call('driver_file', type=str, help='Name of file to deploy')
        deploy_argument_env_call = call('--env', help='Environment to run file in')
        info_argument_env_call = call('--env', action='store_true')

        specific_parser_mock.add_argument.assert_has_calls(
            [
                init_argument_call,
                deploy_argument_env_call,
                deploy_argument_file_call,
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
        global_call = call([])
        project_call = call([['local','/home/local.config.yaml']])
        mock_print.assert_has_calls([global_call, project_call], any_order = True)
    
    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_local_different_environment(self, mock_print):
        self.environment_fetcher_mock.return_value = (['/home/config/uat.config.yaml'], [])
        CommandLineInterface(['info', '--env']).execute()
        global_call = call([])
        project_call = call([['uat','/home/config/uat.config.yaml']])
        mock_print.assert_has_calls([global_call, project_call], any_order = True)
    
    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_global(self, mock_print):
        self.environment_fetcher_mock.return_value = ([], ['/home/config/uat.config.yaml'])
        CommandLineInterface(['info', '--env']).execute()
        global_call = call([['uat', '/home/config/uat.config.yaml']])
        project_call = call([])
        mock_print.assert_has_calls([global_call, project_call], any_order = True)
    
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

    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_returns_correct_error_if_env_not_found(self, mock_find_env):
        mock_find_env.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=local']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `local`. You can list all discoverable environments with `foundations info --envs`")

    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_returns_correct_error_if_env_not_found_different_name(self, mock_find_env):
        mock_find_env.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `uat`. You can list all discoverable environments with `foundations info --envs`")

    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_returns_correct_error_if_wrong_directory(self, mock_find_env):
        mock_find_env.return_value = None
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Foundations project not found. Deploy command must be run in foundations project directory")
     
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploys_job_when_local_config_found(self, mock_find_env):
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_not_called()

    config_manager = let_patch_mock('foundations.global_state.config_manager')
    sys_path = let_patch_mock('sys.path')
    run_file = let_patch_mock('importlib.import_module')

    @let_now
    def os_cwd(self):
        mock = self.patch('os.getcwd')
        mock.return_value = '/path/to/where/ever/we/are'
        return mock

    os_file_exists = let_patch_mock('os.path.isfile')
    os_chdir = let_patch_mock('os.chdir')
    exit_mock = let_patch_mock('sys.exit')
    print_mock = let_patch_mock('builtins.print')
    environment_fetcher_mock = let_patch_mock('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher.get_all_environments')

    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_loads_config_when_found(self, mock_find_env):
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.config_manager.add_simple_config_path.assert_called_with("home/foundations/lou/config/uat.config.yaml")
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_adds_file_to_py_path(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou/'
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/')
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_adds_file_to_py_path_different_path(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/hana/'
        mock_find_env.return_value = ["home/foundations/hana/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/hana/')
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_returns_error_if_driver_file_does_not_exist(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = False
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.py', '--env=uat']).execute()
        self.os_file_exists.assert_called_with('home/foundations/lou/hana/driver.py')
        self.print_mock.assert_called_with('Driver file `hana/driver.py` does not exist')
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_returns_error_if_driver_file_does_not_have_py_extension(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = True
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.exe', '--env=uat']).execute()
        self.print_mock.assert_called_with('Driver file `hana/driver.exe` needs to be a python file with an extension `.py`')

    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_imports_driver_file(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou/'
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.run_file.assert_called_with('driver') 
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_imports_driver_file_different_file(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou'
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hippo/dingo.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/hippo')
        self.run_file.assert_called_with('dingo') 
    
    @patch.object(EnvironmentFetcher, 'find_environment')
    def test_deploy_imports_driver_file_different_name(self, mock_find_env):
        self.os_cwd.return_value = 'home/foundations/lou/'
        mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'passenger.py', '--env=uat']).execute()
        self.run_file.assert_called_with('passenger')    