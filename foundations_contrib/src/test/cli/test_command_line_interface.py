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

from foundations_spec import *

class TestCommandLineInterface(Spec):

    class MockSleep(object):

        _epsilon = 0.0001

        def __init__(self):
            self._time_elapsed = 0
            self.time_to_wait = 0
            self.callback = lambda: None

        def __call__(self, wait_time):
            self._time_elapsed += wait_time
            if self._time_elapsed >= self.time_to_wait - self._epsilon:
                self.callback()

    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')

    @let_now
    def mock_environment(self):
        return self.patch('os.environ', {})

    @let
    def level_1_subparsers_mock(self):
        return Mock()

    @let
    def level_2_subparsers_mock(self):
        return Mock()

    @let
    def level_2_parser_mock(self):
        return Mock()

    @let
    def level_3_parser_mock(self):
        return Mock()

    @let_now
    def mock_contrib_root(self):
        from pathlib import PosixPath

        path = self.faker.uri_path()
        return PosixPath(path)

    mock_subprocess_run = let_patch_mock('subprocess.run')

    def fake_config_path(self, environment):
        return 'home/foundations/lou/config/{}.config.yaml'.format(environment)

    @set_up
    def set_up(self):
        self._server_running = False
        self.psutil_process_mock.side_effect = self._process_constructor
        self.mock_environment['MODEL_SERVER_CONFIG_PATH'] = '/path/to/file'
        self.patch('foundations_contrib.root', return_value=self.mock_contrib_root)
        self.mock_pipeline_context_wrapper = Mock()
        self.mock_pipeline_context_wrapper_class = self.patch('foundations_internal.pipeline_context_wrapper.PipelineContextWrapper', ConditionalReturn())
        self.mock_pipeline_context_wrapper_class.return_when(self.mock_pipeline_context_wrapper, self.current_foundations_context_instance.pipeline_context())

    def test_add_sub_parser_adds_new_subparser(self):
        hello_said = False

        cli = CommandLineInterface(['say_hello'])

        def _callback():
            hello_said = True
        parser = cli.add_sub_parser('say_hello')
        parser.set_defaults(function=_callback)
        cli.execute()

        self.assertTrue(True)

    @patch('argparse.ArgumentParser')
    def test_correct_option_setup(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        parser_mock.add_subparsers.return_value = self.level_1_subparsers_mock

        self.level_1_subparsers_mock.add_parser.return_value = self.level_2_parser_mock
        self.level_2_parser_mock.add_subparsers.return_value = self.level_2_subparsers_mock

        self.level_2_subparsers_mock.add_parser.return_value = self.level_3_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')


        init_call = call('init', help='Creates a new Foundations project in the current directory')
        deploy_call = call('deploy', help='Deploys a Foundations project to the specified environment')
        info_call = call('info', help='Provides information about your Foundations project')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([init_call, deploy_call, info_call], any_order=True)

        init_argument_call = call('project_name', type=str, help='Name of the project to create')
        info_argument_env_call = call('--env', action='store_true')
        
        deploy_argument_file_call = call('--entrypoint', type=str, help='Name of file to deploy (defaults to main.py)')
        deploy_argument_job_directory_call = call('--job-directory', type=str, help='Directory from which to deploy (defaults to cwd)')
        deploy_argument_env_call = call('--env', help='Environment to run file in')
        deploy_argument_project_name_call = call('--project-name', help='Project name for job (optional, defaults to basename(cwd))')
        deploy_argument_num_gpus_call = call('--num-gpus', type=int, help='Number of gpus to allocate for job (defaults to 1)')
        deploy_argument_ram_call = call('--ram', type=float, help='GB of ram to allocate for job (defaults to no limit)')

        self.level_2_parser_mock.add_argument.assert_has_calls(
            [
                init_argument_call,
                info_argument_env_call,
                deploy_argument_env_call,
                deploy_argument_file_call,
                deploy_argument_job_directory_call,
                deploy_argument_project_name_call,
                deploy_argument_num_gpus_call,
                deploy_argument_ram_call
            ],
            any_order=True
        )

    @patch('argparse.ArgumentParser')
    def test_retrieve_artifact_has_correct_options(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        parser_mock.add_subparsers.return_value = self.level_1_subparsers_mock

        self.level_1_subparsers_mock.add_parser.return_value = self.level_2_parser_mock
        self.level_2_parser_mock.add_subparsers.return_value = self.level_2_subparsers_mock

        self.level_2_subparsers_mock.add_parser.return_value = self.level_3_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')

        retrieve_call = call('get', help='Get file types from execution environments')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])
        retrieve_argument_call = call('artifacts', help='Specify type to get as artifact')
        job_id_call = call('--job_id', type=str, required=True, help="Specify job uuid of already deployed job")
        env_call = call('--env', required=True, type=str, help='Environment to get from')
        save_directory_call = call('--save_dir', type=str, default=self.os_cwd(), help="Specify local directory path for artifacts to save to. Defaults to current working directory")
        source_directory_call = call('--source_dir', type=str, default='', help="Specify relative directory path to download artifacts from. Default will download all artifacts from job")

        self.level_2_subparsers_mock.add_parser.assert_has_calls([retrieve_argument_call])
        self.level_3_parser_mock.add_argument.assert_has_calls([job_id_call, env_call, save_directory_call, source_directory_call], any_order=True)

    @patch('argparse.ArgumentParser')
    def test_setup_has_correct_options(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        parser_mock.add_subparsers.return_value = self.level_1_subparsers_mock

        self.level_1_subparsers_mock.add_parser.return_value = self.level_2_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')

        setup_call = call('setup', help='Sets up Foundations for local experimentation')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([setup_call])

    def test_setup_atlas_calls_setup_atlas_script(self):
        CommandLineInterface(['setup', 'atlas']).execute()
        self.mock_subprocess_run.assert_called_with(['bash', './foundations_gui.sh', 'start', 'ui', 'foundations'], cwd=self.mock_contrib_root / 'resources')

    def test_setup_orbit_calls_setup_orbit_script(self):
        CommandLineInterface(['setup', 'orbit']).execute()
        self.mock_subprocess_run.assert_called_with(['bash', './foundations_gui.sh', 'start', 'ui', 'foundations-orbit'], cwd=self.mock_contrib_root / 'resources')

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
        mock_print.assert_called_with([['local','/home/local.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_local_different_environment(self, mock_print):
        self.environment_fetcher_mock.return_value = (['/home/config/uat.config.yaml'], [])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with([['uat','/home/config/uat.config.yaml']])

    @patch.object(CommandLineInterface, '_format_environment_printout')
    def test_info_env_flag_returns_environment_one_available_global(self, mock_print):
        self.environment_fetcher_mock.return_value = ([], ['/home/config/uat.config.yaml'])
        CommandLineInterface(['info', '--env']).execute()
        mock_print.assert_called_with([['uat', '/home/config/uat.config.yaml']])

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

    sys_path = let_patch_mock('sys.path')
    run_file = let_patch_mock('importlib.import_module')

    @let
    def fake_model_server_pid(self):
        import random
        return random.randint(1,65000)

    @let
    def mock_job_id(self):
        return self.faker.uuid4()

    @let
    def mock_model_name(self):
        return f'model-{self.faker.random.randint(1000, 9999)}'

    @let
    def mock_user_provided_model_name(self):
        return self.faker.word()

    @let_now
    def os_cwd(self):
        mock = self.patch('os.getcwd')
        mock.return_value = '/path/to/where/ever/we/are'
        return mock

    def _get_mock_file(self):
        mock_file_object = Mock()
        mock_file_object.__enter__ = lambda x: mock_file_object
        mock_file_object.__exit__ = Mock()
        return mock_file_object

    @let_now
    def mock_pid_file(self):
        return self._get_mock_file()

    @let_now
    def sleep_mock(self):
        return self.patch('time.sleep', self.MockSleep())

    @let
    def fake_save_dir(self):
        return self.faker.uri_path()

    @let
    def fake_source_dir(self):
        return self.faker.uri_path()

    @let
    def fake_env(self):
        return self.faker.word()

    @let
    def fake_job_status(self):
        status = self.faker.word()
        while status == 'queued':
            status = self.faker.word()

        return status

    @let
    def server_startup_time(self):
        from random import random

        between_zero_and_one = random()
        return between_zero_and_one * 2.7 + 0.2

    @let
    def mock_job_deployment(self):
        return Mock()

    @let
    def fake_job_logs(self):
        return self.faker.sentence()

    @let
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext() 

    @let
    def fake_script_file_name(self):
        return '{}.py'.format(self.faker.word())

    @let_now
    def current_foundations_context_instance(self):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.foundations_context import FoundationsContext

        _pipeline = Pipeline(self.pipeline_context)
        foundations_context = FoundationsContext(_pipeline)
        self.current_foundations_context.return_value = foundations_context
        return foundations_context

    @let
    def fake_project_name(self):
        return self.faker.word()

    @let
    def fake_directory(self):
        return self.faker.file_path()

    @let
    def ram(self):
        return self.faker.random.random() * 8 + 0.0001

    @let
    def num_gpus(self):
        return self.faker.random_int(0, 8)

    os_file_exists = let_patch_mock('os.path.isfile')
    os_chdir = let_patch_mock('os.chdir')
    os_kill = let_patch_mock('os.kill')
    subprocess_popen = let_patch_mock('subprocess.Popen')
    print_mock = let_patch_mock('builtins.print')
    exit_mock = let_patch_mock('sys.exit')
    open_mock = let_patch_mock('builtins.open')
    psutil_process_mock = let_patch_mock('psutil.Process')
    server_process = let_mock()
    requests_post_mock = let_patch_mock('requests.post')
    config_manager_mock = let_patch_mock('foundations_contrib.global_state.config_manager')
    environment_fetcher_mock = let_patch_mock('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher.get_all_environments')
    find_environment_mock = let_patch_mock('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher.find_environment')
    artifact_downloader_class_mock = let_patch_mock('foundations_contrib.archiving.artifact_downloader.ArtifactDownloader')
    artifact_downloader_mock = let_mock()
    get_pipeline_archiver_for_job_mock = let_patch_mock('foundations_contrib.archiving.get_pipeline_archiver_for_job')
    pipeline_archiver_mock = let_mock()
    current_foundations_context = let_patch_mock('foundations_contrib.global_state.current_foundations_context')
    mock_deploy_job = let_patch_mock('foundations.job_deployer.deploy_job')
    mock_deploy_model_package = let_patch_mock('foundations_contrib.cli.model_package_server.deploy')
    mock_destroy_model_package = let_patch_mock('foundations_contrib.cli.model_package_server.destroy')
    # orbit
    mock_orbit_deploy_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.deploy')
    mock_orbit_stop_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.stop')
    mock_orbit_destroy_model_package = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.destroy')

    def _process_constructor(self, pid):
        from psutil import NoSuchProcess

        if pid != self.fake_model_server_pid:
            raise AssertionError('process constructor needs to be called with model server pid {} (called with {})'.format(self.fake_model_server_pid, pid))

        if not self._server_running:
            raise NoSuchProcess(pid)

        return self.server_process

    def test_server_deploys_model_server_with_specified_job_id(self):
        CommandLineInterface(['serve', 'start', self.mock_job_id]).execute()
        self.mock_deploy_model_package.assert_called_with(self.mock_job_id)

    def test_deploy_model_serving_logs_event(self):
        CommandLineInterface(['serve', 'start', self.mock_job_id]).execute()
        self.mock_message_router.push_message.assert_called_with('model_served', {'job_id': self.mock_job_id})

    def test_server_destroys_model_server_with_specified_model_name(self):
        CommandLineInterface(['serve', 'stop', self.mock_model_name]).execute()
        self.mock_destroy_model_package.assert_called_with(self.mock_model_name)

    def test_orbit_serve_start_with_specificed_project_model_and_directory(self):
        self._run_model_within_orbit_with_specified_project_name_model_name_project_directory(self.fake_project_name, self.mock_user_provided_model_name, self.fake_directory)
        self.mock_orbit_deploy_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, self.fake_directory, 'local')

    def test_orbit_serve_stop_with_specificed_project_and_model(self):
        self._launch_orbit_with_specified_command_using_project_name_model_name('stop', self.fake_project_name, self.mock_user_provided_model_name)
        self.mock_orbit_stop_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, 'local')

    def test_orbit_serve_destroy_with_specified_project_and_model(self):
        self._launch_orbit_with_specified_command_using_project_name_model_name('destroy', self.fake_project_name, self.mock_user_provided_model_name)
        self.mock_orbit_destroy_model_package.assert_called_with(self.fake_project_name, self.mock_user_provided_model_name, 'local')

    def _run_model_within_orbit_with_specified_project_name_model_name_project_directory(self, project_name, model_name, project_directory):
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

    def test_retrieve_artifacts_calls_environment_fetcher(self):
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.find_environment_mock.assert_called_with(self.fake_env)

    def test_retrieve_artifacts_loads_environment(self):
        fake_env_path = os.path.join(self.faker.uri_path(), self.fake_env)
        self.find_environment_mock.return_value = [fake_env_path]
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with(fake_env_path)

    def test_retrieve_artifacts_fails_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_retrieve_artifacts_prints_error_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Could not find environment `{}`'.format(self.fake_env))

    def test_retrieve_artifacts_gets_pipeline_archiver(self):
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.get_pipeline_archiver_for_job_mock.assert_called_with(self.mock_job_id)

    def test_retrieve_artifacts_creates_archive_downloader(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.artifact_downloader_class_mock.assert_called_with(self.pipeline_archiver_mock)

    def test_retrieve_artifacts_calls_download_files(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        self.artifact_downloader_class_mock.return_value = self.artifact_downloader_mock
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--source_dir={}'.format(self.fake_source_dir), '--save_dir={}'.format(self.fake_save_dir)]).execute()
        self.artifact_downloader_mock.download_files.assert_called_with(self.fake_source_dir, self.fake_save_dir)

    def test_deploy_forwards_default_arguments_to_command_line_job_deployer(self):
        self.patch('foundations_contrib.cli.command_line_job_deployer.CommandLineJobDeployer', MockCommandLineJobDeployer)

        expected_arguments = Mock()
        expected_arguments.env = None
        expected_arguments.job_directory = None
        expected_arguments.entrypoint = None
        expected_arguments.project_name = None
        expected_arguments.ram = None
        expected_arguments.num_gpus = None

        CommandLineInterface(['deploy']).execute()
        arguments = MockCommandLineJobDeployer.arguments

        self._assert_arguments_equal(expected_arguments, arguments)

    def test_deploy_forwards_specified_arguments_to_command_line_job_deployer(self):
        self.patch('foundations_contrib.cli.command_line_job_deployer.CommandLineJobDeployer', MockCommandLineJobDeployer)

        expected_arguments = Mock()
        expected_arguments.env = self.fake_env
        expected_arguments.job_directory = self.fake_directory
        expected_arguments.entrypoint = self.fake_script_file_name
        expected_arguments.project_name = self.fake_project_name
        expected_arguments.ram = self.ram
        expected_arguments.num_gpus = self.num_gpus

        command_to_run = [
            'deploy',
            f'--env={self.fake_env}',
            f'--job-directory={self.fake_directory}',
            f'--entrypoint={self.fake_script_file_name}',
            f'--project-name={self.fake_project_name}',
            f'--ram={self.ram}',
            f'--num-gpus={self.num_gpus}'
        ]

        CommandLineInterface(command_to_run).execute()
        arguments = MockCommandLineJobDeployer.arguments

        self._assert_arguments_equal(expected_arguments, arguments)

    @patch('argparse.ArgumentParser')
    def test_retrieve_logs_has_correct_options(self, parser_class_mock):
        parser_mock = Mock()
        parser_class_mock.return_value = parser_mock

        parser_mock.add_subparsers.return_value = self.level_1_subparsers_mock

        self.level_1_subparsers_mock.add_parser.return_value = self.level_2_parser_mock
        self.level_2_parser_mock.add_subparsers.return_value = self.level_2_subparsers_mock

        self.level_2_subparsers_mock.add_parser.return_value = self.level_3_parser_mock

        CommandLineInterface([])

        parser_class_mock.assert_called_with(prog='foundations')
        parser_mock.add_argument.assert_called_with('--version', action='store_true', help='Displays the current Foundations version')

        retrieve_call = call('get', help='Get file types from execution environments')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])
        retrieve_argument_call = call('logs', help='Get logs for jobs')
        job_id_call = call('--job_id', type=str, required=True, help="Specify job uuid of already deployed job")
        env_call = call('--env', required=True, type=str, help='Environment to get from')

        self.level_2_subparsers_mock.add_parser.assert_has_calls([retrieve_argument_call])
        self.level_3_parser_mock.add_argument.assert_has_calls([job_id_call, env_call], any_order=True)

    def test_get_job_logs_for_environment_that_does_not_exist_prints_error_message(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_any_call('Error: Could not find environment `{}`'.format(self.fake_env))

    def test_get_job_logs_for_environment_that_does_not_exist_exits_with_code_1(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_prints_error_message(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` does not exist for environment `{}`'.format(self.mock_job_id, self.fake_env))

    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_exits_with_code_1(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_queued_job_prints_error_message(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` is queued and has not produced any logs'.format(self.mock_job_id))

    def test_get_job_logs_for_queued_job_exits_with_code_1(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_job_that_exists_and_is_not_queued_prints_logs(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with(self.fake_job_logs)

    def test_get_job_logs_for_job_that_exists_and_is_not_queued_does_not_call_exit(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_not_called()

    def _assert_arguments_equal(self, expected_arguments, actual_arguments):
        for attribute_name in ['env', 'job_directory', 'entrypoint', 'project_name', 'ram', 'num_gpus']:
            self.assertEqual(getattr(expected_arguments, attribute_name), getattr(actual_arguments, attribute_name))

    def _set_run_script_environment(self, environment_to_set):
        self.config_manager_mock.__getitem__ = ConditionalReturn()
        self.config_manager_mock.__getitem__.return_when(environment_to_set, 'run_script_environment')

    def _set_job_status(self, status):
        self.mock_job_deployment.get_job_status.return_value = status

        mock_job_deployment_class = ConditionalReturn()
        mock_job_deployment_class.return_when(self.mock_job_deployment, self.mock_job_id, None, None)

        mock_get_item = ConditionalReturn()
        mock_get_item.return_when({'deployment_type': mock_job_deployment_class}, 'deployment_implementation')
        self.config_manager_mock.__getitem__ = mock_get_item

class MockCommandLineJobDeployer(object):
    arguments = None
    deploy_called = False

    def __init__(self, arguments):
        MockCommandLineJobDeployer.arguments = arguments

    def deploy(self):
        MockCommandLineJobDeployer.deploy_called = True