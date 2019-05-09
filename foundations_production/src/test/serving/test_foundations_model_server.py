"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers import let, let_now, let_patch_mock, set_up
from foundations_spec.helpers.spec import Spec


class TestFoundationsModelServer(Spec):

    os_remove = let_patch_mock('os.remove')
    open_mock = let_patch_mock('builtins.open')
    os_getpid_mock = let_patch_mock('os.getpid')
    os_path_exists = let_patch_mock('os.path.exists')
    flask_mock = let_patch_mock('flask.Flask')

    @let_now
    def mock_pid_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda x: mock_file
        mock_file.__exit__ = Mock()
        return mock_file
    
    
    @set_up
    def set_up(self):
        self.flask_app_mock = Mock()
        self.flask_mock.return_value = self.flask_app_mock
        self.os_path_exists.return_value = True

    def test_foundations_model_server_run_calls_os_remove(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()
        self.os_remove.assert_called_with(FoundationsModelServer.pid_file_path)


    def test_foundations_model_server_run_method_creates_pid_file(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()
        self.open_mock.assert_called_with(FoundationsModelServer.pid_file_path, 'w')


    def test_foundations_model_server_run_calls_os_remove(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()
        self.os_path_exists.assert_called_with(FoundationsModelServer.pid_file_path)

    def test_foundations_model_server_run_method_writes_current_process_pid_to_pid_file(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        self.open_mock.return_value = self.mock_pid_file
        self.os_getpid_mock.return_value = 123
        model_server = FoundationsModelServer()
        model_server.run()
        self.mock_pid_file.write.assert_called_with('123')

    def test_foundations_model_server_run_method_creates_flask_application(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        self.open_mock.return_value = self.mock_pid_file
        model_server = FoundationsModelServer()
        model_server.run()
        self.flask_mock.assert_called_with('foundations_production.serving.foundations_model_server')

    def test_foundations_model_server_run_method_runs_flask_application(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        model_server = FoundationsModelServer()
        model_server.run()
        self.flask_app_mock.run.assert_called()

    def test_foundations_model_server_does_not_start_if_pid_file_cannot_be_created(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        get_logger_mock = self.patch('logging.getLogger')
        self.open_mock.side_effect = OSError
        model_server = FoundationsModelServer()
        model_server.run()
        self.os_path_exists.assert_not_called()
        self.flask_app_mock.run.assert_not_called()

    def test_foundations_model_server_logs_error_if_flask_does_not_run(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        get_logger_mock = self.patch('logging.getLogger')
        logger = Mock()
        get_logger_mock.return_value = logger
        self.flask_app_mock.run.side_effect = OSError('Fake error')
        model_server = FoundationsModelServer()
        model_server.run()
        logger.error.assert_called_with('Fake error')

    def test_foundations_model_server_loads_routes(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        load_routes_mock = self.patch('foundations_production.serving.model_server_routes.load_routes')
        model_server = FoundationsModelServer()
        model_server.run()
        load_routes_mock.assert_called_with(self.flask_app_mock)
