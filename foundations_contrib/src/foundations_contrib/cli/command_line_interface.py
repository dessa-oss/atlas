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
        from foundations_contrib.cli.sub_parsers.orbit_parser import OrbitParser
        from foundations_contrib.cli.sub_parsers.monitor_parser import MonitorParser
        from foundations_contrib.cli.sub_parsers.atlas_parser import AtlasParser
        
        self._input_arguments = args

        self._argument_parser = self._initialize_argument_parser()
        self._subparsers = self._argument_parser.add_subparsers()

        self._initialize_init_parser()
        self._initialize_info_parser()

        SetupParser(self).add_sub_parser()
        OrbitParser(self).add_sub_parser()
        MonitorParser(self).add_sub_parser()
        AtlasParser(self).add_sub_parser()

    def add_sub_parser(self, name, help=None):
        sub_parser = self._subparsers.add_parser(name, help=help)
        sub_parser.add_argument('--debug', action='store_true', help='Sets debug mode for the CLI')
        return sub_parser

    def _initialize_argument_parser(self):
        from argparse import ArgumentParser
        argument_parser = ArgumentParser(prog='foundations')
        argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        argument_parser.add_argument('--debug', action='store_true', help='Sets debug mode for the CLI')
        argument_parser.set_defaults(function=self._no_command)
        return argument_parser

    def _initialize_init_parser(self):
        init_parser = self.add_sub_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)

    @staticmethod
    def _str_to_bool(string_value):
        return string_value == 'True'

    def _initialize_info_parser(self):
        info_parser = self.add_sub_parser('info', help='Provides information about your Foundations project')
        info_parser.add_argument('--env', action='store_true')
        info_parser.set_defaults(function=self._info)

    def _initialize_model_serve_parser(self):
        serving_parser = self.add_sub_parser('serve', help='Used to serve models in Atlas')
        serving_subparsers = serving_parser.add_subparsers()

        serving_deploy_parser = serving_subparsers.add_parser('start')
        serving_deploy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_deploy_parser.add_argument('job_id')
        serving_deploy_parser.set_defaults(function=self._kubernetes_model_serving_deploy)

        serving_destroy_parser = serving_subparsers.add_parser('stop')
        serving_destroy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_destroy_parser.add_argument('model_name')
        serving_destroy_parser.set_defaults(function=self._kubernetes_model_serving_destroy)

    def _initialize_serving_stop_parser(self, serving_subparsers):
        serving_deploy_parser = serving_subparsers.add_parser('stop', help='Stop foundations model package server')
        serving_deploy_parser.set_defaults(function=self._model_serving_stop)

    def execute(self):
        from foundations_contrib.global_state import log_manager

        self._arguments = self._argument_parser.parse_args(self._input_arguments)
        try:
            self._arguments.function()
        except Exception as error:
            if self._arguments.debug == True:
                raise
            else:
                print(f'Error running command: {error}')
                exit(1)

    def arguments(self):
        return self._arguments

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
            self._print_configs('submission', global_environment)
            if project_environment != None:
                self._print_configs('execution', project_environment)

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
        import os
        environment_names = []
        for env in available_environments:
            environment_names.append([env.split(os.path.sep)[-1].split('.')[0], env])
        return environment_names

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

    def _deploy_model_package(self):
        import requests
        import sys

        response = requests.post('http://{}/v1/{}/'.format(self._arguments.domain, self._arguments.slug), json = {'model_id': self._arguments.model_id})
        if response.status_code == 201:
            print('Model package was deployed successfully to model server.')
        else:
            print('Failed to deploy model package to model server.', file=sys.stderr)
            sys.exit(11)

    def _kubernetes_model_serving_deploy(self):
        from foundations_contrib.cli.model_package_server import deploy
        from foundations_contrib.global_state import message_router

        message_router.push_message('model_served', {'job_id': self._arguments.job_id, 'project_name': self._arguments.project_name})
        deploy(self._arguments.project_name, self._arguments.job_id)

    def _kubernetes_model_serving_destroy(self):
        from foundations_contrib.cli.model_package_server import destroy
        destroy(self._arguments.project_name, self._arguments.model_name)
