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
    argument_parser_class_mock = let_patch_mock('argparse.ArgumentParser')        

    @let_now
    def mock_pid_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda x: mock_file
        mock_file.__exit__ = Mock()
        return mock_file

    def _get_rest_api_server_mock(self):
        rest_api_server_mock = Mock()
        rest_api_server_class_mock = self.patch('foundations_production.serving.rest_api_server.RestAPIServer')
        rest_api_server_class_mock.return_value = rest_api_server_mock
        return rest_api_server_mock
    
    @set_up
    def set_up(self):
        self.flask_app_mock = Mock()
        self.flask_mock.return_value = self.flask_app_mock
        self.os_path_exists.return_value = True

        self.parser_mock = Mock()
        self.argument_parser_class_mock.return_value = self.parser_mock
        self.parsed_arguments_mock = Mock()
        self.parser_mock.parse_args.return_value = self.parsed_arguments_mock

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
        self.flask_mock.assert_called_with('foundations_production.serving.rest_api_server')

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

    def test_foundations_model_server_runs_rest_api_server(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        rest_api_server_mock = self._get_rest_api_server_mock()
        model_server = FoundationsModelServer()
        model_server.run()
        rest_api_server_mock.run.assert_called()

    def test_foundations_model_server_argument_parser_class_has_description(self):
        from foundations_production.serving.foundations_model_server import main

        self.parsed_arguments_mock.domain = 'some_domain:1234'
        main()
        self.argument_parser_class_mock.assert_called_with(description='starts foundations model server')


    def test_foundations_model_server_gets_domain_and_port_from_cli(self):
        from foundations_production.serving.foundations_model_server import main

        self.parsed_arguments_mock.domain = ''
        main()
        self.parser_mock.add_argument.assert_called_with('--domain', type=str, help='domain and port used by foundations model server')

    def test_foundations_model_server_passes_domain_and_port_to_rest_api_server_run_method(self):
        from foundations_production.serving.foundations_model_server import main

        self.parsed_arguments_mock.domain = 'some_domain:1234'
        rest_api_server_mock = self._get_rest_api_server_mock()
        main()
        self.parser_mock.parse_args.assert_called()
        rest_api_server_mock.run.assert_called_with(host='some_domain', port=1234)

    