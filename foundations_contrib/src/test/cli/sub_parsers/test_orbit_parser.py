"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_contrib.cli.sub_parsers.orbit_parser import OrbitParser
from foundations_contrib.cli.command_line_interface import CommandLineInterface


class TestOrbitParser(Spec):

    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')
    mock_subprocess_run = let_patch_mock('subprocess.run')
    mock_orbit_deploy_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.deploy')
    mock_orbit_stop_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.stop')
    mock_orbit_destroy_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.destroy')

    @let_now
    def mock_contrib_root(self):
        from pathlib import PosixPath
        path = self.faker.uri_path()
        return PosixPath(path)

    @let
    def fake_project_name(self):
        return self.faker.word()

    @let
    def fake_directory(self):
        return self.faker.file_path()

    @let
    def mock_user_provided_model_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.patch('foundations_contrib.root', return_value=self.mock_contrib_root)

    def test_sub_parser_retrieves_command_line_interface_as_parameter(self):
        cli = CommandLineInterface([''])
        orbit_sub_parser = OrbitParser(cli)
        self.assertTrue(type(orbit_sub_parser._cli) is CommandLineInterface)

    def test_sub_parser_setup_parser_on_cli_instantiation(self):
        mock_add_parser = self.patch('foundations_contrib.cli.sub_parsers.orbit_parser.OrbitParser.add_sub_parser')
        CommandLineInterface([''])
        mock_add_parser.assert_called_once()

    def test_sub_parser_called_specifically_for_orbit(self):
        mock_argument_parser = self.patch('foundations_contrib.cli.command_line_interface.CommandLineInterface.add_sub_parser')
        CommandLineInterface([''])
        help_msg = 'Provides operations for managing projects and models in Orbit'
        mock_argument_parser.assert_any_call('orbit', help=help_msg)

    def test_orbit_sub_parser_is_triggered_when_orbit_command_is_provided(self):
        mock_deploy = self.patch('foundations_contrib.cli.sub_parsers.orbit_parser.OrbitParser._kubernetes_orbit_model_serving_deploy')
        self._run_orbit_with_project_name_model_name_project_directory('project', 'model', 'dir')
        mock_deploy.assert_called_once()

    def test_orbit_serve_start_with_specified_project_model_and_directory(self):
        self._run_orbit_with_project_name_model_name_project_directory(self.fake_project_name, self.mock_user_provided_model_name, self.fake_directory)
        self.mock_orbit_deploy_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, self.fake_directory, 'local')

    def test_orbit_serve_stop_with_specified_project_and_model(self):
        self._launch_orbit_with_specified_command_using_project_name_model_name('stop', self.fake_project_name, self.mock_user_provided_model_name)
        self.mock_orbit_stop_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, 'local')

    def test_orbit_serve_destroy_with_specified_project_and_model(self):
        self._launch_orbit_with_specified_command_using_project_name_model_name('destroy', self.fake_project_name, self.mock_user_provided_model_name)
        self.mock_orbit_destroy_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, 'local')

    def _run_orbit_with_project_name_model_name_project_directory(self, project_name, model_name, project_directory):
        CommandLineInterface([
            'orbit',
            'serve',
            'start',
            '--project_name={}'.format(project_name),
            '--model_name={}'.format(model_name),
            '--project_directory={}'.format(project_directory)
        ]).execute()

    def _launch_orbit_with_specified_command_using_project_name_model_name(self, command, project_name, model_name):
        CommandLineInterface([
            'orbit',
            'serve',
            command,
            '--project_name={}'.format(project_name),
            '--model_name={}'.format(model_name)
        ]).execute()

