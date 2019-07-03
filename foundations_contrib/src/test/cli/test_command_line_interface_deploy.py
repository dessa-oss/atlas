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

class TestCommandLineInterfaceDeploy(Spec):

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

    scaffold_project_mock = let_patch_mock('foundations_contrib.cli.scaffold.Scaffold.scaffold_project')

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
    mock_set_job_resources = let_patch_mock('foundations.set_job_resources')

    def _process_constructor(self, pid):
        from psutil import NoSuchProcess

        if pid != self.fake_model_server_pid:
            raise AssertionError('process constructor needs to be called with model server pid {} (called with {})'.format(self.fake_model_server_pid, pid))

        if not self._server_running:
            raise NoSuchProcess(pid)

        return self.server_process

    def test_exits_the_process_with_exit_status_of_one(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=non-existant-env']).execute()
        self.exit_mock.assert_called_with(1)

    def test_does_not_exit_when_environments_exist(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.exit_mock.assert_not_called()

    def test_deploy_returns_correct_error_if_wrong_directory(self):
        self.find_environment_mock.return_value = None
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Foundations project not found. Deploy command must be run in foundations project directory")
        self.exit_mock.assert_called_with(1)

    def test_deploys_job_when_local_config_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.print_mock.assert_not_called()

    def test_deploy_returns_correct_error_if_env_not_found(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=local']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `local`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_deploy_returns_correct_error_if_env_not_found_different_name(self):
        self.find_environment_mock.return_value = []
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.print_mock.assert_called_with("Could not find environment name: `uat`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`")
        self.exit_mock.assert_called_with(1)

    def test_deploy_loads_config_when_found(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with("home/foundations/lou/config/uat.config.yaml")

    def test_deploy_adds_file_to_py_path(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/')

    def test_deploy_adds_file_to_py_path_different_path(self):
        self.os_cwd.return_value = 'home/foundations/hana/'
        self.find_environment_mock.return_value = ["home/foundations/hana/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/hana/')

    def test_deploy_returns_error_if_driver_file_does_not_exist(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = False
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=hana/driver.py', '--env=uat']).execute()
        self.os_file_exists.assert_called_with('home/foundations/lou/hana/driver.py')
        self.print_mock.assert_called_with('Driver file `hana/driver.py` does not exist')
        self.exit_mock.assert_called_with(1)

    def test_deploy_returns_error_if_driver_file_does_not_have_py_extension(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.os_file_exists.return_value = True
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=hana/driver.exe', '--env=uat']).execute()
        self.print_mock.assert_called_with('Driver file `hana/driver.exe` needs to be a python file with an extension `.py`')
        self.exit_mock.assert_called_with(1)

    def test_deploy_imports_driver_file(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.run_file.assert_called_with('driver')

    def test_deploy_imports_driver_file_different_file(self):
        self.os_cwd.return_value = 'home/foundations/lou'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=hippo/dingo.py', '--env=uat']).execute()
        self.sys_path.append.assert_called_with('home/foundations/lou/hippo')
        self.run_file.assert_called_with('dingo')

    def test_deploy_imports_driver_file_different_name(self):
        self.os_cwd.return_value = 'home/foundations/lou/'
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=passenger.py', '--env=uat']).execute()
        self.run_file.assert_called_with('passenger')
    
    def test_foundations_deploy_project_name_is_default_if_not_set(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat']).execute()
        self.assertEqual('default', self.pipeline_context.provenance.project_name)

    def test_foundations_deploy_project_name_is_set_if_provided(self):
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint=driver.py', '--env=uat', '--project-name={}'.format(self.fake_project_name)]).execute()
        self.assertEqual(self.fake_project_name, self.pipeline_context.provenance.project_name)

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()
        self.assertEqual(self.fake_script_file_name, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_False_when_driver_nested(self):
        import os.path as path

        script_path = path.join(self.fake_directory, self.fake_script_file_name)

        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(script_path), '--env=uat']).execute()

        self.assertEqual(script_path, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_not_set_when_driver_nested(self):
        import os.path as path

        script_path = path.join(self.fake_directory, self.fake_script_file_name)

        self._set_run_script_environment({})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(script_path), '--env=uat']).execute()

        self.assertEqual(script_path, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_does_not_chdir_if_enable_stages_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.os_chdir.assert_not_called()

    def test_foundations_deploy_does_not_append_to_syspath_if_enable_stages_False(self):
        self._set_run_script_environment({'enable_stages': False})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.sys_path.append.assert_not_called()

    def test_foundations_deploy_sets_script_to_run_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})
        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()
        self.assertEqual(self.fake_script_file_name, self.config_manager_mock['run_script_environment']['script_to_run'])

    def test_foundations_deploy_deploys_stageless_job_with_job_deployer_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.mock_deploy_job.assert_called_with(self.mock_pipeline_context_wrapper, None, {})

    def test_foundations_deploy_deploys_stageless_job_with_job_deployer_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.mock_deploy_job.assert_called_with(self.mock_pipeline_context_wrapper, None, {})

    def test_foundations_deploy_does_not_deploy_job_with_stages_if_enable_stages_is_False(self):
        self._set_run_script_environment({'enable_stages': False})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.run_file.assert_not_called()

    def test_foundations_deploy_does_not_deploy_job_with_stages_if_enable_stages_is_not_set(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.run_file.assert_not_called()

    def test_foundations_deploy_with_ram_set_sets_amount_of_ram(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat', '--ram={}'.format(self.ram)]).execute()

        self.mock_set_job_resources.assert_called_with(ram=self.ram)

    def test_foundations_deploy_with_num_gpus_set_sets_amount_of_gpus(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat', '--num-gpus={}'.format(self.num_gpus)]).execute()

        self.mock_set_job_resources.assert_called_with(num_gpus=self.num_gpus)

    def test_foundations_deploy_with_both_ram_and_num_gpus_set_sets_both(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat', '--num-gpus={}'.format(self.num_gpus), '--ram={}'.format(self.ram)]).execute()

        self.mock_set_job_resources.assert_called_with(ram=self.ram, num_gpus=self.num_gpus)

    def test_foundations_deploy_with_neither_ram_nor_gpus_does_not_set_either(self):
        self._set_run_script_environment({})

        self.find_environment_mock.return_value = ["home/foundations/lou/config/uat.config.yaml"]
        CommandLineInterface(['deploy', '--entrypoint={}'.format(self.fake_script_file_name), '--env=uat']).execute()

        self.mock_set_job_resources.assert_not_called()

    def test_foundations_deploy_with_env_not_specified_uses_local_config_yaml_in_global_configs_if_it_exists(self):
        from os.path import expanduser

        local_config_file_path = expanduser('~/.foundations/config/local.config.yaml')
        self.find_environment_mock.return_value = [local_config_file_path]
        CommandLineInterface(['deploy', '--entrypoint=driver.py']).execute()
        self.config_manager_mock.add_simple_config_path.assert_called_with(local_config_file_path)

    def test_foundations_deploy_with_env_not_specified_prints_error_if_local_config_yaml_does_not_exist_in_global_configs(self):
        from os.path import expanduser

        CommandLineInterface(['deploy', '--entrypoint=driver.py']).execute()
        self.print_mock.assert_called_with('Could not find environment name: `local`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`')

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
