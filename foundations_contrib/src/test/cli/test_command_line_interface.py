"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_contrib.cli.command_line_interface import CommandLineInterface

class TestCommandLineInterface(unittest.TestCase):
    
    @patch('argparse.ArgumentParser')
    def test_correct_option_setup(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        sub_parsers_mock = Mock()
        parser_mock.add_subparsers.return_value = sub_parsers_mock

        init_parser_mock = Mock()
        sub_parsers_mock.add_parser.return_value = init_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')
        sub_parsers_mock.add_parser.assert_called_with('init', help='Creates a new Foundations project in the current directory')
        init_parser_mock.add_argument.assert_called_with('project_name', type=str, help='Name of the project to create')

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
