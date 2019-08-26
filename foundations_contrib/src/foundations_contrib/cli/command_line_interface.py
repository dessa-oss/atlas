"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from tabulate import tabulate

class CommandLineInterface(object):

    def __init__(self, args):
        from foundations_contrib.cli.sub_parsers.setup_parser import SetupParser

        self._input_arguments = args

        self._argument_parser = self._initialize_argument_parser()
        self._subparsers = self._argument_parser.add_subparsers()

        SetupParser(self).add_sub_parser()
        self._initialize_init_parser()
        self._initialize_deploy_parser()
        self._initialize_info_parser()
        self._initialize_model_serve_parser()
        self._initialize_retrieve_parser()
        self._initialize_orbit_model_serve_parser()

    def add_sub_parser(self, name, help=None):
        return self._subparsers.add_parser(name, help=help)

    def _initialize_argument_parser(self):
        from argparse import ArgumentParser
        argument_parser = ArgumentParser(prog='foundations')
        argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        argument_parser.set_defaults(function=self._no_command)
        return argument_parser

    def _initialize_init_parser(self):
        init_parser = self.add_sub_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)

    def _initialize_deploy_parser(self):
        deploy_parser = self.add_sub_parser('deploy', help='Deploys a Foundations project to the specified environment')
        deploy_parser.add_argument('--entrypoint', type=str, help='Name of file to deploy (defaults to main.py)')
        deploy_parser.add_argument('--env', help='Environment to run file in')
        deploy_parser.add_argument('--project-name', help='Project name for job (optional, defaults to basename(cwd))')
        deploy_parser.add_argument('--job-directory', type=str, help='Directory from which to deploy (defaults to cwd)')
        deploy_parser.add_argument('--num-gpus', type=int, help='Number of gpus to allocate for job (defaults to 1)')
        deploy_parser.add_argument('--ram', type=float, help='GB of ram to allocate for job (defaults to no limit)')
        deploy_parser.set_defaults(function=self._deploy)

    def _initialize_info_parser(self):
        info_parser = self.add_sub_parser('info', help='Provides information about your Foundations project')
        info_parser.add_argument('--env', action='store_true')
        info_parser.set_defaults(function=self._info)

    def _initialize_model_serve_parser(self):
        serving_parser = self.add_sub_parser('serve', help='Used to serve models in Atlas')
        serving_subparsers = serving_parser.add_subparsers()

        serving_deploy_parser = serving_subparsers.add_parser('start')
        serving_deploy_parser.add_argument('job_id')
        serving_deploy_parser.set_defaults(function=self._kubernetes_model_serving_deploy)

        serving_destroy_parser = serving_subparsers.add_parser('stop')
        serving_destroy_parser.add_argument('model_name')
        serving_destroy_parser.set_defaults(function=self._kubernetes_model_serving_destroy)

    def _initialize_retrieve_parser(self):
        retrieve_parser = self.add_sub_parser('get', help='Get file types from execution environments')
        retrieve_subparsers = retrieve_parser.add_subparsers()
        self._initialize_retrieve_artifact_parser(retrieve_subparsers)
        self._initialize_retrieve_logs_parser(retrieve_subparsers)

    def _initialize_retrieve_artifact_parser(self, retrieve_subparsers):
        from os import getcwd

        retrieve_artifact_parser = retrieve_subparsers.add_parser('artifacts', help='Specify type to get as artifact')
        retrieve_artifact_parser.add_argument('--job_id', required=True, type=str, help="Specify job uuid of already deployed job")
        retrieve_artifact_parser.add_argument('--env', required=True, type=str, help='Environment to get from')
        retrieve_artifact_parser.add_argument('--save_dir', type=str, default=getcwd(), help="Specify local directory path for artifacts to save to. Defaults to current working directory")
        retrieve_artifact_parser.add_argument('--source_dir', type=str, default='', help="Specify relative directory path to download artifacts from. Default will download all artifacts from job")
        retrieve_artifact_parser.set_defaults(function=self._retrieve_artifacts)

    def _initialize_retrieve_logs_parser(self, retrieve_subparsers):
        retrieve_logs_parser = retrieve_subparsers.add_parser('logs', help='Get logs for jobs')
        retrieve_logs_parser.add_argument('--job_id', required=True, type=str, help='Specify job uuid of already deployed job')
        retrieve_logs_parser.add_argument('--env', required=True, type=str, help='Environment to get from')
        retrieve_logs_parser.set_defaults(function=self._retrieve_logs)

    def _initialize_serving_stop_parser(self, serving_subparsers):
        serving_deploy_parser = serving_subparsers.add_parser('stop', help='Stop foundations model package server')
        serving_deploy_parser.set_defaults(function=self._model_serving_stop)

    def _initialize_orbit_model_serve_parser(self):
        orbit_parser = self.add_sub_parser('orbit', help='Provides operations for managing projects and models in Orbit')
        orbit_subparsers = orbit_parser.add_subparsers()

        serving_parser = orbit_subparsers.add_parser('serve')
        serving_subparsers = serving_parser.add_subparsers()

        serving_deploy_parser = serving_subparsers.add_parser('start')
        serving_deploy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_deploy_parser.add_argument('--model_name', required=True, type=str, help='The unique name of the model within the project')
        serving_deploy_parser.add_argument('--project_directory', required=True, type=str, help='The location of the code and resources used to define the model')
        serving_deploy_parser.add_argument('--env', required=False, type=str, help='Specifies the execution environment where jobs are ran')
        serving_deploy_parser.set_defaults(function=self._kubernetes_orbit_model_serving_deploy)

        serving_stop_parser = serving_subparsers.add_parser('stop')
        serving_stop_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_stop_parser.add_argument('--model_name', required=True, type=str, help='The unique name of the model within the project')
        serving_stop_parser.set_defaults(function=self._kubernetes_orbit_model_serving_stop)

        serving_destroy_parser = serving_subparsers.add_parser('destroy')
        serving_destroy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_destroy_parser.add_argument('--model_name', required=True, type=str, help='The unique name of the model within the project')
        serving_destroy_parser.set_defaults(function=self._kubernetes_orbit_model_serving_destroy)


    def execute(self):
        self._arguments = self._argument_parser.parse_args(self._input_arguments)
        self._arguments.function()

    def _no_command(self):
        import foundations

        if self._arguments.version:
            print('Running Foundations version {}'.format(foundations.__version__))
        else:
            self._argument_parser.print_help()

    def _init(self):
        from foundations_contrib.cli.scaffold import Scaffold

        project_name = self._arguments.project_name
        result = Scaffold(project_name).scaffold_project()
        if result:
            print('Success: New Foundations project `{}` created!'.format(project_name))
        else:
            print('Error: project directory for `{}` already exists'.format(project_name))

    def _info(self):
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

        env_name = self._arguments.env

        if not env_name:
            print('usage: foundations info [--env ENV]')
            return

        project_environment, global_environment = EnvironmentFetcher().get_all_environments()

        if len(global_environment) == 0 and (project_environment == None or len(project_environment) == 0):
            print('No environments available')
        else:
            self._print_configs('global', global_environment)
            if project_environment != None:
                self._print_configs('project', project_environment)

    def _print_configs(self, config_list_name, config_list):
        config_list = self._create_environment_list(config_list)
        print("\n{} configs:".format(config_list_name))
        if len(config_list) == 0:
            print('No {} environments available'.format(config_list_name))
        else:
            print(self._format_environment_printout(config_list))

    def _format_environment_printout(self, environment_array):
        return tabulate(environment_array, headers = ['env_name', 'env_path'])

    def _create_environment_list(self, available_environments):
        environment_names = []
        for env in available_environments:
            environment_names.append([env.split('/')[-1].split('.')[0], env])
        return environment_names

    def _deploy(self):
        from foundations_contrib.cli.command_line_job_deployer import CommandLineJobDeployer
        CommandLineJobDeployer(self._arguments).deploy()
   
    def _model_serving_stop(self):
        import os
        import signal

        if self._is_model_server_running():
            pid = self._get_model_server_pid()
            os.kill(int(pid), signal.SIGTERM)
            self._remove_pid_file()

    def _retrieve_artifacts(self):
        from foundations_contrib.archiving.artifact_downloader import ArtifactDownloader
        from foundations_contrib.archiving import get_pipeline_archiver_for_job

        self._load_configuration()

        pipeline_archiver = get_pipeline_archiver_for_job(self._arguments.job_id)
        artifact_downloader = ArtifactDownloader(pipeline_archiver)
        artifact_downloader.download_files(self._arguments.source_dir, self._arguments.save_dir)

    def _retrieve_logs(self):
        from foundations_contrib.global_state import config_manager

        env_name = self._arguments.env
        job_id = self._arguments.job_id
        self._load_configuration()

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._fail_with_message('Error: Job `{}` does not exist for environment `{}`'.format(job_id, env_name))
        elif job_status == 'queued':
            self._fail_with_message('Error: Job `{}` is queued and has not produced any logs'.format(job_id))
        else:
            logs = job_deployment.get_job_logs()
            print(logs)

    def _load_configuration(self):
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
        from foundations_contrib.global_state import config_manager

        env_name = self._arguments.env
        env_file_path = EnvironmentFetcher().find_environment(env_name)

        if env_file_path and env_file_path[0]:
            config_manager.add_simple_config_path(env_file_path[0])
        else:
            self._fail_with_message('Error: Could not find environment `{}`'.format(env_name))

    def _fail_with_message(self, message):
        import sys

        print(message)
        sys.exit(1)

    def _start_model_server_if_not_running(self):
        import subprocess
        import sys
        import os

        if self._is_model_server_running():
            print('Model server is already running.')
        else:
            model_server_config_path = os.environ['MODEL_SERVER_CONFIG_PATH']

            subprocess_command_to_run = [
                'python', '-m', 'foundations_production.serving.foundations_model_server',
                '--domain={}'.format(self._arguments.domain),
                '--config-file={}'.format(model_server_config_path)
            ]

            subprocess.Popen(subprocess_command_to_run, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            self._wait_for_model_server_to_start()
            if not self._is_model_server_running():
                print('Failed to start model server.', file=sys.stderr)
                sys.exit(10)

    def _wait_for_model_server_to_start(self):
        from time import sleep

        max_attempts = 30
        attempts = 1
        while attempts < max_attempts and not self._is_model_server_running():
            sleep(0.1)
            attempts += 1

    def _deploy_model_package(self):
        import requests
        import sys

        response = requests.post('http://{}/v1/{}/'.format(self._arguments.domain, self._arguments.slug), json = {'model_id': self._arguments.model_id})
        if response.status_code == 201:
            print('Model package was deployed successfully to model server.')
        else:
            print('Failed to deploy model package to model server.', file=sys.stderr)
            sys.exit(11)

    def _is_model_server_running(self):
        from psutil import NoSuchProcess

        try:
            pid = self._get_model_server_pid()
            command_line = self._get_model_server_command_line(pid)
            return 'foundations_production.serving.foundations_model_server' in command_line
        except (OSError, NoSuchProcess):
            return False

    def _get_model_server_pid(self):
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        with open(FoundationsModelServer.pid_file_path, 'r') as pidfile:
            return pidfile.read()

    def _remove_pid_file(self):
        from os import remove
        from foundations_production.serving.foundations_model_server import FoundationsModelServer

        try:
            remove(FoundationsModelServer.pid_file_path)
        except OSError:
            pass

    def _get_model_server_command_line(self, pid):
        import psutil

        process = psutil.Process(int(pid))
        return process.cmdline()

    def _kubernetes_model_serving_deploy(self):
        from foundations_contrib.cli.model_package_server import deploy
        from foundations_contrib.global_state import message_router

        message_router.push_message('model_served', {'job_id': self._arguments.job_id})
        deploy(self._arguments.job_id)

    def _kubernetes_model_serving_destroy(self):
        from foundations_contrib.cli.model_package_server import destroy
        destroy(self._arguments.model_name)

    def _kubernetes_orbit_model_serving_deploy(self):
        from foundations_contrib.cli.orbit_model_package_server import deploy
        from foundations_contrib.global_state import message_router

        env = self._arguments.env if self._arguments.env is not None else 'local'

        successfully_added = deploy(self._arguments.project_name, self._arguments.model_name, self._arguments.project_directory, env)

        if successfully_added:
            message_router.push_message('project_model_served', {
                'project_name': self._arguments.project_name,
                'model_name': self._arguments.model_name,
                'project_directory': self._arguments.project_directory
            })
        # else:
        #     message = f'Error: model {self._arguments.model_name} exists in project {self._arguments.project_name}. Aborting'
        #     self._fail_with_message(message)

    def _kubernetes_orbit_model_serving_stop(self):
        from foundations_contrib.cli.orbit_model_package_server import stop
        successfully_stopped = stop(self._arguments.project_name, self._arguments.model_name)

    def _kubernetes_orbit_model_serving_destroy(self):
        from foundations_contrib.cli.orbit_model_package_server import destroy
        successfully_destroy = destroy(self._arguments.project_name, self._arguments.model_name)