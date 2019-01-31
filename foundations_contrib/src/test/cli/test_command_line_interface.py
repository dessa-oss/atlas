"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch, call

from foundations_contrib.cli.command_line_interface import CommandLineInterface
from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

class TestCommandLineInterface(unittest.TestCase):
    
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
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_execute_spits_out_version(self, mock_print):
        CommandLineInterface(['--version']).execute()
        mock_print.assert_called_with('Running Foundations version 3.2.54')

    @patch('foundations.__version__', '7.3.3')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_execute_spits_out_version_different_version(self, mock_print):
        CommandLineInterface(['--version']).execute()
        mock_print.assert_called_with('Running Foundations version 7.3.3')
        
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print', lambda *args: None)
    def test_scaffold_creates_scaffold_with_project_name(self, scaffold_mock):
        CommandLineInterface(['init', 'my project']).execute()
        scaffold_mock.assert_called_with('my project')
        
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print', lambda *args: None)
    def test_scaffold_creates_scaffold_with_project_name_different_project(self, scaffold_mock):
        CommandLineInterface(['init', 'my different project']).execute()
        scaffold_mock.assert_called_with('my different project')
        
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print', lambda *args: None)
    def test_scaffold_scaffolds_with_project_name_different_project(self, scaffold_mock):
        scaffold_instance = Mock()
        scaffold_mock.return_value = scaffold_instance

        CommandLineInterface(['init', 'my project']).execute()
        scaffold_instance.scaffold_project.assert_called()
            
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_scaffold_prints_success_message(self, mock_print, scaffold_mock):
        scaffold_instance = Mock()
        scaffold_mock.return_value = scaffold_instance
        scaffold_instance.scaffold_project.return_value = True

        CommandLineInterface(['init', 'my project']).execute()
        mock_print.assert_called_with('Success: New Foundations project `my project` created!')
            
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_scaffold_prints_success_message_different_project(self, mock_print, scaffold_mock):
        scaffold_instance = Mock()
        scaffold_mock.return_value = scaffold_instance
        scaffold_instance.scaffold_project.return_value = True

        CommandLineInterface(['init', 'your project']).execute()
        mock_print.assert_called_with('Success: New Foundations project `your project` created!')
            
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_scaffold_prints_failure_message(self, mock_print, scaffold_mock):
        scaffold_instance = Mock()
        scaffold_mock.return_value = scaffold_instance
        scaffold_instance.scaffold_project.return_value = False

        CommandLineInterface(['init', 'my project']).execute()
        mock_print.assert_called_with('Error: project directory for `my project` already exists')
            
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_scaffold_prints_failure_message_different_project(self, mock_print, scaffold_mock):
        scaffold_instance = Mock()
        scaffold_mock.return_value = scaffold_instance
        scaffold_instance.scaffold_project.return_value = False

        CommandLineInterface(['init', 'your project']).execute()
        mock_print.assert_called_with('Error: project directory for `your project` already exists')
    
    @patch.object(EnvironmentFetcher, 'get_all_environments')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_info_env_flag_returns_environment_none_available(self, mock_print, environment_fetcher_mock):
        environment_fetcher_mock.return_value = []
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with('No environments available')
    
    @patch.object(EnvironmentFetcher, 'get_all_environments')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_info_env_flag_returns_environment_one_available(self, mock_print, environment_fetcher_mock):
        environment_fetcher_mock.return_value = ['/home/local.config.yaml']
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with({'local'})
    
    @patch.object(EnvironmentFetcher, 'get_all_environments')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_info_env_flag_returns_environment_local_and_global_available(self, mock_print, environment_fetcher_mock):
        environment_fetcher_mock.return_value = ['/home/local.config.yaml', '~/foundations/local.config.yaml']
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with({'local'})

    @patch.object(EnvironmentFetcher, 'find_environment')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_deploy_returns_correct_error_if_env_not_found(self, mock_print, mock_find_env):
        mock_find_env.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=local']).execute()
        mock_print.assert_called_with("Could not find environment name: `local`. You can list all discoverable environments with `foundations info --envs`")

    @patch.object(EnvironmentFetcher, 'find_environment')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_deploy_returns_correct_error_if_env_not_found_different_name(self, mock_print, mock_find_env):
        mock_find_env.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        mock_print.assert_called_with("Could not find environment name: `uat`. You can list all discoverable environments with `foundations info --envs`")

    @patch.object(EnvironmentFetcher, 'find_environment')
    @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    def test_deploy_returns_correct_error_if_wrong_directory(self, mock_print, mock_find_env):
        mock_find_env.return_value = "Wrong directory"
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        mock_print.assert_called_with("Foundations project not found. Deploy command must be run in foundations project directory")
     
    # @patch.object(EnvironmentFetcher, 'find_environment')
    # @patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.static_print')
    # def test_deploys_job_when_local_config_found(self, mock_print, mock_find_env):
    #     mock_find_env.return_value = ["home/foundations/lou/config/uat.config.yaml"]
    #     CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
    #     mock_print.assert_called_with("Job deployed")

#want a local prioritization test
#driver file not found  