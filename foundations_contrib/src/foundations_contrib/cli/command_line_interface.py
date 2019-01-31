"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CommandLineInterface(object):

    @staticmethod
    def static_print(*args, **kwargs):
        print(*args, **kwargs)
    
    def __init__(self, args):
        from argparse import ArgumentParser

        self._argument_parser = ArgumentParser(prog='foundations')
        self._argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        self._argument_parser.set_defaults(function=self._no_command)
        subparsers = self._argument_parser.add_subparsers()
        
        init_parser = subparsers.add_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)

        deploy_parser = subparsers.add_parser('deploy', help='Deploys a Foundations project to the specified environment')
        deploy_parser.add_argument('driver_file', type=str, help='Name of file to deploy')
        deploy_parser.add_argument('--env', help='Environment to run file in')
        deploy_parser.set_defaults(function=self._deploy)

        info_parser = subparsers.add_parser('info', help='Provides information about your Foundations project')
        info_parser.add_argument('--env', action='store_true')
        info_parser.set_defaults(function=self._info)
        
        
        self._arguments = self._argument_parser.parse_args(args)

    def execute(self):
        self._arguments.function()

    def _no_command(self):
        import foundations

        if self._arguments.version:
            CommandLineInterface.static_print('Running Foundations version {}'.format(foundations.__version__))
        else:
            self._argument_parser.print_help()

    def _init(self):
        from foundations_contrib.cli.scaffold import Scaffold
        
        project_name = self._arguments.project_name
        result = Scaffold(project_name).scaffold_project()
        if result:
            CommandLineInterface.static_print('Success: New Foundations project `{}` created!'.format(project_name))
        else:
            CommandLineInterface.static_print('Error: project directory for `{}` already exists'.format(project_name))
        
    def _info(self):
        import re
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

        available_environments = EnvironmentFetcher().get_all_environments()

        environment_names = []

        for env in available_environments:
            environment_names.append(env.split('/')[-1].split('.')[0])
        if len(environment_names) == 0:
            CommandLineInterface.static_print('No environments available')
        else:
            CommandLineInterface.static_print(set(environment_names))
        
    def _deploy(self):
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

        env_name = self._arguments.env
        env_file_path = EnvironmentFetcher().find_environment(env_name)

        if env_file_path == "Wrong directory":
            CommandLineInterface.static_print("Foundations project not found. Deploy command must be run in foundations project directory"  )
        else:
            CommandLineInterface.static_print("Could not find environment name: `{}`. You can list all discoverable environments with `foundations info --envs`".format(env_name))
