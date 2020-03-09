
import faker
from unittest import mock
from unittest.mock import patch
from foundations_spec import *
from foundations_core_cli.command_line_interface import CommandLineInterface
from foundations_atlas_cli.sub_parsers.atlas.atlas_parser import AtlasParser

class TestAtlasParser(Spec):

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

    sys_path = let_patch_mock('sys.path')
    run_file = let_patch_mock('importlib.import_module')

    os_file_exists = let_patch_mock('os.path.isfile')
    os_chdir = let_patch_mock('os.chdir')
    os_kill = let_patch_mock('os.kill')
    subprocess_popen = let_patch_mock('subprocess.Popen')
    print_mock = let_patch_mock('builtins.print')
    exit_mock = let_patch_mock('sys.exit')
    open_mock = let_patch_mock('builtins.open')
    server_process = let_mock()
    requests_post_mock = let_patch_mock('requests.post')
    config_manager_mock = let_patch_mock('foundations_contrib.global_state.config_manager')
    environment_fetcher_mock = let_patch_mock('foundations_core_cli.environment_fetcher.EnvironmentFetcher.get_all_environments')
    find_environment_mock = let_patch_mock('foundations_core_cli.environment_fetcher.EnvironmentFetcher.find_environment')
    artifact_downloader_class_mock = let_patch_mock('foundations_contrib.archiving.artifact_downloader.ArtifactDownloader')
    artifact_downloader_mock = let_mock()
    get_pipeline_archiver_for_job_mock = let_patch_mock('foundations_contrib.archiving.get_pipeline_archiver_for_job')
    pipeline_archiver_mock = let_mock()
    mock_deploy_job = let_patch_mock('foundations_contrib.job_deployer.deploy_job')

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

    @let
    def command(self):
        return self.faker.word()

    def fake_config_path(self, environment):
        return 'home/foundations/lou/config/{}.config.yaml'.format(environment)

    def test_sub_parser_retrieves_command_line_interface_as_parameter(self):
        cli = CommandLineInterface([''])
        atlas_sub_parser = AtlasParser(cli)
        self.assertTrue(type(atlas_sub_parser._cli) is CommandLineInterface)

    def test_sub_parser_setup_parser_on_cli_instantiation(self):
        mock_add_parser = self.patch('foundations_atlas_cli.sub_parsers.atlas.atlas_parser.AtlasParser.add_sub_parser')
        CommandLineInterface([''])
        mock_add_parser.assert_called_once()

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
        
        version_call = call('--version', action='store_true', help='Displays the current Foundations version')
        debug_call = call('--debug', action='store_true', help='Sets debug mode for the CLI')

        parser_mock.add_argument.assert_has_calls(
            [
                version_call,
                debug_call
            ]
        )

        retrieve_call = call('get', help='Get file types from execution environments')
        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])

        retrieve_argument_call = call('job', help='Specify job to retrieve artifacts from')
        job_id_call = call('job_id', type=str, help='Specify job uuid of already deployed job')
        env_call = call('scheduler_config', type=str, help='Environment to get from')
        save_directory_call = call('--save_dir', type=str, default=None, help='Specify local directory path for artifacts to save to. Defaults to directory within current working directory')
        source_directory_call = call('--source_dir', type=str, default='', help='Specify relative directory path to download artifacts from. Default will download all artifacts from job')

        self.level_2_subparsers_mock.add_parser.assert_has_calls([retrieve_argument_call])
        self.level_3_parser_mock.add_argument.assert_has_calls(
            [
                job_id_call,
                env_call,
                save_directory_call,
                source_directory_call
            ],
            any_order=True
        )

    @quarantine
    def test_retrieve_artifacts_calls_environment_fetcher(self):
        CommandLineInterface(['get', 'job', self.fake_env, self.mock_job_id]).execute()
        self.find_environment_mock.assert_called_with(self.fake_env)

    @quarantine
    def test_retrieve_artifacts_loads_environment(self):
        fake_env_path = os.path.join(self.faker.uri_path(), self.fake_env)
        self.find_environment_mock.return_value = [fake_env_path]
        CommandLineInterface(['get', 'job', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with(fake_env_path)

    def test_retrieve_artifacts_fails_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'job', self.fake_env, self.mock_job_id]).execute()
        self.exit_mock.assert_called_with(1)

    @quarantine
    def test_retrieve_artifacts_prints_error_if_missing_environment(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Could not find environment `{}`'.format(self.fake_env))

    @quarantine
    def test_retrieve_artifacts_gets_pipeline_archiver(self):
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.get_pipeline_archiver_for_job_mock.assert_called_with(self.mock_job_id)

    @quarantine
    def test_retrieve_artifacts_creates_archive_downloader(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id)]).execute()
        self.artifact_downloader_class_mock.assert_called_with(self.pipeline_archiver_mock)

    @quarantine
    def test_retrieve_artifacts_calls_download_files(self):
        self.get_pipeline_archiver_for_job_mock.return_value = self.pipeline_archiver_mock
        self.artifact_downloader_class_mock.return_value = self.artifact_downloader_mock
        CommandLineInterface(['get', 'artifacts', '--job_id={}'.format(self.mock_job_id), '--source_dir={}'.format(self.fake_source_dir), '--save_dir={}'.format(self.fake_save_dir)]).execute()
        self.artifact_downloader_mock.download_files.assert_called_with(self.fake_source_dir, self.fake_save_dir)

    def test_submit_forwards_default_arguments_to_command_line_job_submission(self):
        self.patch('foundations_core_cli.job_submission.submit_job.submit', MockCommandLineJobDeployer)

        expected_arguments = Mock()
        expected_arguments.scheduler_config = None
        expected_arguments.job_directory = None
        expected_arguments.entrypoint = None
        expected_arguments.project_name = None
        expected_arguments.ram = None
        expected_arguments.num_gpus = None
        expected_arguments.stream_job_logs = True
        expected_arguments.command = None

        CommandLineInterface(['submit']).execute()
        arguments = MockCommandLineJobDeployer.arguments

        self._assert_submit_arguments_equal(expected_arguments, arguments)

    def test_submit_forwards_specified_arguments_to_command_line_job_submission(self):
        self.patch('foundations_core_cli.job_submission.submit_job.submit', MockCommandLineJobDeployer)

        expected_arguments = Mock()
        expected_arguments.scheduler_config = self.fake_env
        expected_arguments.job_directory = self.fake_directory
        expected_arguments.entrypoint = self.fake_script_file_name
        expected_arguments.project_name = self.fake_project_name
        expected_arguments.ram = self.ram
        expected_arguments.num_gpus = self.num_gpus
        expected_arguments.stream_job_logs = False
        expected_arguments.command = [self.command]

        command_to_run = [
            'submit',
            f'--entrypoint={self.fake_script_file_name}',
            f'--project-name={self.fake_project_name}',
            f'--ram={self.ram}',
            f'--num-gpus={self.num_gpus}',
            f'--stream-job-logs=False',
            self.fake_env,
            self.fake_directory,
            self.command
        ]

        CommandLineInterface(command_to_run).execute()
        arguments = MockCommandLineJobDeployer.arguments

        self._assert_submit_arguments_equal(expected_arguments, arguments)

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
        
        version_call = call('--version', action='store_true', help='Displays the current Foundations version')
        debug_call = call('--debug', action='store_true', help='Sets debug mode for the CLI')

        parser_mock.add_argument.assert_has_calls(
            [
                version_call,
                debug_call
            ]
        )

        retrieve_call = call('get', help='Get file types from execution environments')

        self.level_1_subparsers_mock.add_parser.assert_has_calls([retrieve_call])
        retrieve_argument_call = call('logs', help='Get logs for jobs')
        job_id_call = call('scheduler_config', type=str, help='Environment to get from')
        env_call = call('job_id', type=str, help='Specify job uuid of already deployed job')

        self.level_2_subparsers_mock.add_parser.assert_has_calls([retrieve_argument_call])
        self.level_3_parser_mock.add_argument.assert_has_calls(
            [
                job_id_call,
                env_call
            ],
            any_order=True
        )

    @quarantine
    def test_get_job_logs_for_environment_that_does_not_exist_prints_error_message(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_any_call('Error: Could not find environment `{}`'.format(self.fake_env))

    def test_get_job_logs_for_environment_that_does_not_exist_exits_with_code_1(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['get', 'logs', self.fake_env, self.mock_job_id]).execute()
        self.exit_mock.assert_called_with(1)

    @quarantine
    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_prints_error_message(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` does not exist for environment `{}`'.format(self.mock_job_id, self.fake_env))

    def test_get_job_logs_for_environment_that_exists_for_job_that_does_not_exist_exits_with_code_1(self):
        self._set_job_status(None)

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', self.fake_env, self.mock_job_id]).execute()
        self.exit_mock.assert_called_with(1)

    @quarantine
    def test_get_job_logs_for_queued_job_prints_error_message(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with('Error: Job `{}` is queued and has not produced any logs'.format(self.mock_job_id))

    @quarantine
    def test_get_job_logs_for_queued_job_exits_with_code_1(self):
        self._set_job_status('queued')

        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_called_with(1)

    @quarantine
    def test_get_job_logs_for_job_that_exists_and_is_not_queued_prints_logs(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.print_mock.assert_called_with(self.fake_job_logs)

    @quarantine
    def test_get_job_logs_for_job_that_exists_and_is_not_queued_does_not_call_exit(self):
        self._set_job_status(self.fake_job_status)
        self.mock_job_deployment.get_job_logs.return_value = self.fake_job_logs
        self.find_environment_mock.return_value = [self.fake_config_path(self.fake_env)]
        CommandLineInterface(['get', 'logs', '--job_id={}'.format(self.mock_job_id), '--env={}'.format(self.fake_env)]).execute()
        self.exit_mock.assert_not_called()

    def _assert_deploy_arguments_equal(self, expected_arguments, actual_arguments):
        for attribute_name in ['env', 'job_directory', 'entrypoint', 'project_name', 'ram', 'num_gpus']:
            self.assertEqual(getattr(expected_arguments, attribute_name), getattr(actual_arguments, attribute_name))

    def _assert_submit_arguments_equal(self, expected_arguments, actual_arguments):
        for attribute_name in ['scheduler_config', 'job_directory', 'entrypoint', 'project_name', 'ram', 'num_gpus', 'stream_job_logs', 'command']:
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
