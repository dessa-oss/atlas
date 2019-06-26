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
from foundations_production.serving.foundations_model_server import FoundationsModelServer
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
        serving_call = call('serving', help='Start serving a model package')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([init_call, deploy_call, info_call, serving_call], any_order=True)

        init_argument_call = call('project_name', type=str, help='Name of the project to create')
        deploy_argument_file_call = call('driver_file', type=str, help='Name of file to deploy')
        deploy_argument_env_call = call('--env', help='Environment to run file in')
        deploy_argument_project_name_call = call('--project_name', help='Project name for job (optional, defaults to "default")')
        info_argument_env_call = call('--env', action='store_true')

        self.level_2_parser_mock.add_argument.assert_has_calls(
            [
                init_argument_call,
                deploy_argument_env_call,
                deploy_argument_file_call,
                deploy_argument_project_name_call,
                info_argument_env_call,
            ],
            any_order=True
        )

        serving_deploy_call = call('deploy', help='Deploy model package to foundations model package server')
        self.level_2_subparsers_mock.add_parser.assert_has_calls([serving_deploy_call], any_order=True)

        serving_deploy_rest_call = call('rest', help='Uses REST format content type')
        serving_deploy_domain_call = call('--domain', type=str, help='Domain and port of the model package server')
        serving_deploy_model_id_call = call('--model-id', type=str, help='Model package ID')
        serving_deploy_slug_call = call('--slug', type=str, help='Model package namespace string')

        self.level_3_parser_mock.add_argument.assert_has_calls(
            [
                serving_deploy_rest_call,
                serving_deploy_domain_call,
                serving_deploy_model_id_call,
                serving_deploy_slug_call,
            ]
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

        retrieve_call = call('retrieve', help='Retrieve file types from execution environments')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])
        retrieve_argument_call = call('artifacts', help='Specify type to retrieve as artifact')
        job_id_call = call('--job_id', type=str, required=True, help="Specify job uuid of already deployed job")
        env_call = call('--env', required=True, type=str, help='Environment to retrieve from')
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

    def test_setup_calls_setup_script(self):
        CommandLineInterface(['setup']).execute()
        self.mock_subprocess_run.assert_called_with(['bash', './foundations_gui.sh', 'start', 'ui'], cwd=self.mock_contrib_root / 'resources')

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

    def test_deploy_returns_correct_error_if_env_not_found(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=local']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `local`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_deploy_returns_correct_error_if_env_not_found_different_name(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `uat`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_exits_the_process_with_exit_status_of_one(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', 'driver.py', '--env=non-existant-env']).execute()
        self.exit_mock.assert_called_with(1)

    def test_does_not_exit_when_environments_exist(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.exit_mock.assert_not_called()

    def test_deploy_returns_correct_error_if_wrong_directory(self):
        self.find_environment_mock.return_value = None
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Foundations project not found. Deploy command must be run in foundations project directory")
        self.exit_mock.assert_called_with(1)

    def test_deploys_job_when_local_config_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.print_mock.assert_not_called()

    sys_path = let_patch_mock('sys.path')
    run_file = let_patch_mock('importlib.import_module')

    @let
    def fake_model_server_pid(self):
        import random
        return random.randint(1,65000)

    @let
    def mock_job_id(self):
        return self.faker.uuid4()

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

    def _process_constructor(self, pid):
        from psutil import NoSuchProcess

        if pid != self.fake_model_server_pid:
            raise AssertionError('process constructor needs to be called with model server pid {} (called with {})'.format(self.fake_model_server_pid, pid))

        if not self._server_running:
            raise NoSuchProcess(pid)

        return self.server_process

    def test_deploy_loads_config_when_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with("home/foundations/lou/config/uat.config.yaml")

    def test_deploy_adds_file_to_py_path(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/')

    def test_deploy_adds_file_to_py_path_different_path(self):
        self.os_cwd.return_value = 'home/foundations/hana/'
        self.find_environment_mock.return_value = ["home/foundations/hana/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/hana/')

    def test_deploy_returns_error_if_driver_file_does_not_exist(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = False
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.py', '--env=uat']).execute()
        self.os_file_exists.assert_called_with('home/foundations/lou/hana/driver.py')
        self.print_mock.assert_called_with('Driver file `hana/driver.py` does not exist')
        self.exit_mock.assert_called_with(1)

    def test_deploy_returns_error_if_driver_file_does_not_have_py_extension(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = True
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hana/driver.exe', '--env=uat']).execute()
        self.print_mock.assert_called_with('Driver file `hana/driver.exe` needs to be a python file with an extension `.py`')
        self.exit_mock.assert_called_with(1)

    def test_deploy_imports_driver_file(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.run_file.assert_called_with('driver')

    def test_deploy_imports_driver_file_different_file(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'hippo/dingo.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/hippo')
        self.run_file.assert_called_with('dingo')

    def test_deploy_imports_driver_file_different_name(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'passenger.py', '--env=uat']).execute()
        self.run_file.assert_called_with('passenger')

    def test_serving_deploy_rest_opens_pid_file(self):
        self._create_server_pidfile()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.open_mock.assert_any_call(FoundationsModelServer.pid_file_path, 'r')

    def test_serving_deploy_rest_reads_pid_file(self):
        self._create_server_pidfile()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.mock_pid_file.read.assert_called()

    def test_serving_deploy_rest_prints_message_if_web_server_is_already_running(self):
        self._bring_server_up()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_any_call('Model server is already running.')

    def test_serving_deploy_rest_runs_model_server_when_server_is_not_running(self):
        from subprocess import DEVNULL

        self._create_server_pidfile()
        self.server_process.cmdline.return_value = ['another_process.py']
        self._server_running = True
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=/path/to/file'], stdout=DEVNULL, stderr=DEVNULL)

    def test_serving_deploy_rest_starts_model_server_when_there_is_no_pidfile_and_process_not_running(self):
        from subprocess import DEVNULL

        self.open_mock.side_effect = OSError()

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=/path/to/file'], stdout=DEVNULL, stderr=DEVNULL)

    def test_serving_deploy_rest_starts_model_server_when_there_is_no_pidfile_and_process_not_running_different_model_config(self):
        from subprocess import DEVNULL

        self.open_mock.side_effect = OSError()
        self.mock_environment['MODEL_SERVER_CONFIG_PATH'] = 'a/path/to/another/file'

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.subprocess_popen.assert_called_with(['python', '-m', 'foundations_production.serving.foundations_model_server', '--domain=localhost:8000', '--config-file=a/path/to/another/file'], stdout=DEVNULL, stderr=DEVNULL)

    def test_serving_deploy_rest_calls_prints_failure_message_if_server_fails_to_run(self):
        self.open_mock.side_effect = OSError()

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_any_call('Failed to start model server.', file=sys.stderr)
        self.exit_mock.assert_any_call(10)

    def test_serving_deploy_rest_calls_deploy_model_rest_api_if_server_is_running(self):
        self._bring_server_up()
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        url = 'http://{}/v1/{}/'.format('localhost:8000', 'snail')
        self.requests_post_mock.assert_called_with(url, json = {'model_id':'some_id'})

    def test_serving_deploy_rest_informs_user_if_model_package_was_deployed_successfully(self):
        self._bring_server_up()
        response_mock = Mock()
        response_mock.status_code = 201
        self.requests_post_mock.return_value = response_mock
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_called_with('Model package was deployed successfully to model server.')

    def test_serving_deploy_rest_informs_user_if_model_package_failed_to_be_deployed(self):
        self._bring_server_up()
        response_mock = Mock()
        response_mock.status_code = 500
        self.requests_post_mock.return_value = response_mock
        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.print_mock.assert_called_with('Failed to deploy model package to model server.', file=sys.stderr)
        self.exit_mock.assert_called_with(11)

    def test_serving_stop_kills_model_server(self):
        import signal

        self._bring_server_up()
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_called_once_with(self.fake_model_server_pid, signal.SIGINT)

    def test_serving_stop_does_not_kill_server_if_it_is_not_up(self):
        self.open_mock.side_effect = OSError()
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_not_called()

    def test_serving_stop_does_not_kill_process_if_it_is_model_server_process(self):
        self._create_server_pidfile()
        self.server_process.cmdline.return_value = ['another_process.py']
        self._server_running = True
        CommandLineInterface(['serving', 'stop']).execute()
        self.os_kill.assert_not_called()

    def test_cli_does_not_fail_if_model_server_starts_before_900_ms(self):
        self.open_mock.side_effect = OSError()
        response_mock = Mock()
        response_mock.status_code = 201
        self.requests_post_mock.return_value = response_mock

        self.sleep_mock.time_to_wait = self.server_startup_time
        self.sleep_mock.callback = self._bring_server_up

        CommandLineInterface(['serving', 'deploy', 'rest', '--domain=localhost:8000', '--model-id=some_id', '--slug=snail']).execute()
        self.exit_mock.assert_not_called()

    def test_retrieve_artifacts_calls_environment_fetcher(self):
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.find_environment_mock.assert_called_with(self.fake_env)

    def test_retrieve_artifacts_loads_environment(self):
        fake_env_path = os.path.join(self.faker.uri_path(), self.fake_env)
        self.find_environment_mock.return_value = [fake_env_path]
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with(fake_env_path)

    def test_retrieve_artifacts_fails_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_retrieve_artifacts_prints_error_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Could not find environment `{}`'.format(self.fake_env))

    def test_retrieve_artifacts_gets_pipeline_archiver(self):
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.get_pipeline_archiver_for_job_mock.assert_called_with(self.mock_job_id)

    def test_retrieve_artifacts_creates_archive_downloader(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.artifact_downloader_class_mock.assert_called_with(self.pipeline_archiver_mock)

    def test_retrieve_artifacts_calls_download_files(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        self.artifact_downloader_class_mock.return_value = self.artifact_downloader_mock
        CommandLineInterface(['retrieve', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--source_dir={}'.format(self.fake_source_dir), '--save_dir={}'.format(self.fake_save_dir)]).execute()
        self.artifact_downloader_mock.download_files.assert_called_with(self.fake_source_dir, self.fake_save_dir)

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

        retrieve_call = call('retrieve', help='Retrieve file types from execution environments')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])
        retrieve_argument_call = call('logs', help='Get logs for jobs')
        job_id_call = call('--job_id', type=str, required=True, help="Specify job uuid of already deployed job")
        env_call = call('--env', required=True, type=str, help='Environment to retrieve from')

        self.level_2_subparsers_mock.add_parser.assert_has_calls([retrieve_argument_call])
        self.level_3_parser_mock.add_argument.assert_has_calls([job_id_call, env_call], any_order=True)

    def test_get_job_logs_for_environment_that_does_not_exist_prints_error_message(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_any_call('Error: Could not find environment `{}`'.format(self.fake_env))

    def test_get_job_logs_for_environment_that_does_not_exist_exits_with_code_1(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_prints_error_message(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` does not exist for environment `{}`'.format(self.mock_job_id, self.fake_env))

    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_exits_with_code_1(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_queued_job_prints_error_message(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` is queued and has not produced any logs'.format(self.mock_job_id))

    def test_get_job_logs_for_queued_job_exits_with_code_1(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    def test_get_job_logs_for_job_that_exists_and_is_not_queued_prints_logs(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with(self.fake_job_logs)

    def test_get_job_logs_for_job_that_exists_and_is_not_queued_does_not_call_exit(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['retrieve', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_not_called()

    def test_foundations_deploy_project_name_is_default_if_not_set(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat']).execute()
        self.assertEqual('default', self.pipeline_context.provenance.project_name)

    def test_foundations_deploy_project_name_is_set_if_provided(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', 'driver.py', '--env=uat', '--project_name={}'.format(self.fake_project_name)]).execute()
        self.assertEqual(self.fake_project_name, self.pipeline_context.provenance.project_name)

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()
        self.assertEqual(self.fake_script_file_name, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_False_when_driver_nested(self):
        import os.path as path

        script_path = path.join(self.fake_directory, self.fake_script_file_name)

        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', script_path, '--env=uat']).execute()

        self.assertEqual(script_path, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_not_set_when_driver_nested(self):
        import os.path as path

        script_path = path.join(self.fake_directory, self.fake_script_file_name)

        self._set_run_script_environment({})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', script_path, '--env=uat']).execute()

        self.assertEqual(script_path, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_does_not_chdir_if_enable_stages_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.os_chdir.assert_not_called()

    def test_foundations_deploy_does_not_append_to_syspath_if_enable_stages_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.sys_path.append.assert_not_called()

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()
        self.assertEqual(self.fake_script_file_name, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_deploys_stageless_job_with_job_deployer_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.mock_deploy_job.assert_called_with(self.mock_pipeline_context_wrapper, None, {})

    def test_foundations_deploy_deploys_stageless_job_with_job_deployer_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.mock_deploy_job.assert_called_with(self.mock_pipeline_context_wrapper, None, {})

    def test_foundations_deploy_does_not_deploy_job_with_stages_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.run_file.assert_not_called()

    def test_foundations_deploy_does_not_deploy_job_with_stages_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', self.fake_script_file_name, '--env=uat']).execute()

        self.run_file.assert_not_called()

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

    def _bring_server_up(self):
        self._create_server_pidfile()
        self._spawn_server_process()

    def _spawn_server_process(self):
        self.server_process.cmdline.return_value = ['foundations_production.serving.foundations_model_server']
        self._server_running = True

    def _create_server_pidfile(self):
        self.mock_pid_file.read.return_value = '{}'.format(self.fake_model_server_pid)
        self.open_mock = self.patch('builtins.open', ConditionalReturn())
        self.open_mock.return_when(self.mock_pid_file, FoundationsModelServer.pid_file_path, 'r')
