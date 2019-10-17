"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_contrib.cli.command_line_interface import CommandLineInterface
from foundations_contrib.cli.sub_parsers.monitor_parser import MonitorParser

class TestMonitorParser(Spec):

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
        cmd = 'monitor pause'
        CommandLineInterface(cmd.split()).execute()
        mock_method.assert_called_once()