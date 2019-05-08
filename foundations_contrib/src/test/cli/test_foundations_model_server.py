"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers import let, let_now, let_patch_mock
from foundations_spec.helpers.spec import Spec


class TestFoundationsModelServer(Spec):

    open_mock = let_patch_mock('builtins.open')
    os_getpid_mock = let_patch_mock('os.getpid')
    flask_mock = let_patch_mock('flask.Flask')

    def test_foundations_model_server_creates_pid_file(self):
        from foundations_contrib.cli.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()
        self.open_mock.assert_called_with('/tmp/foundations_model_server.pid', 'w')

    def test_foundations_model_server_writes_current_process_pid_to_pid_file(self):
        from foundations_contrib.cli.foundations_model_server import FoundationsModelServer

        mock_pid_file = Mock()
        mock_pid_file.__enter__ = lambda x: mock_pid_file
        mock_pid_file.__exit__ = Mock()
        self.open_mock.return_value = mock_pid_file
        self.os_getpid_mock.return_value = 123
        model_server = FoundationsModelServer()
        model_server.run()
        mock_pid_file.write.assert_called_with('123')

    def test_foundations_model_server_creates_flask_application(self):
        from foundations_contrib.cli.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()

        self.flask_mock.assert_called_with('foundations_contrib.cli.foundations_model_server')


    def test_foundations_model_server_runs_flask_application(self):
        from foundations_contrib.cli.foundations_model_server import FoundationsModelServer

        flask_app_mock = Mock()
        self.flask_mock.return_value = flask_app_mock
        model_server = FoundationsModelServer()
        model_server.run()
        flask_app_mock.run.assert_called()

        