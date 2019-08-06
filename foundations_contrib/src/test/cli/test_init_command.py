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

from foundations_contrib.cli.init_command import InitCommand
from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
from foundations_production.serving.foundations_model_server import FoundationsModelServer
from foundations import ConfigManager

from foundations_spec import *

class TestInitCommand(Spec):
    @patch('foundations_contrib.cli.scaffold.Scaffold')
    def test_scaffold_creates_scaffold_with_project_name(self, scaffold_mock):
        InitCommand(['init', 'my project']).execute()
        scaffold_mock.assert_called_with('my project') 
