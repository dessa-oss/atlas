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