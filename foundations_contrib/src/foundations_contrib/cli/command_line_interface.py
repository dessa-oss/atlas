"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from tabulate import tabulate

class CommandLineInterface(object):

    def __init__(self, args):
        self._argument_parser = self._initialize_argument_parser()
        subparsers = self._argument_parser.add_subparsers()

        self._initialize_init_parser(subparsers)
        self._initialize_deploy_parser(subparsers)
        self._initialize_info_parser(subparsers)
      
        self._arguments = self._argument_parser.parse_args(args)
        
    def _initialize_argument_parser(self): 
        from argparse import ArgumentParser
        argument_parser = ArgumentParser(prog='foundations')
        argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        argument_parser.set_defaults(function=self._no_command)
        return argument_parser
    
    def _initialize_init_parser(self, subparsers):
        init_parser = subparsers.add_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)

    def _initialize_deploy_parser(self, subparsers):
        deploy_parser = subparsers.add_parser('deploy', help='Deploys a Foundations project to the specified environment')
        deploy_parser.add_argument('driver_file', type=str, help='Name of file to deploy')
        deploy_parser.add_argument('--env', help='Environment to run file in')
        deploy_parser.set_defaults(function=self._deploy)
    
    def _initialize_info_parser(self, subparsers):
        info_parser = subparsers.add_parser('info', help='Provides information about your Foundations project')
        info_parser.add_argument('--env', action='store_true')
        info_parser.set_defaults(function=self._info)

    def execute(self):
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

        project_environment, global_environment = EnvironmentFetcher().get_all_environments()

        if len(global_environment) == 0 and (project_environment == None or len(project_environment) == 0):
            print('None')
        else:
            self._print_configs('global', global_environment)
            if project_environment != None: 
                self._print_configs('project', project_environment)

    def _print_configs(self, config_list_name, config_list):
        config_list = self._create_environment_list(config_list)
        print("{} configs:".format(config_list_name))
        print(self._format_environment_printout(config_list))
    
    def _format_environment_printout(self, environment_array):
        return tabulate(environment_array, headers = ['env_name', 'env_path'])
    
    def _create_environment_list(self, available_environments):
        environment_names = []
        for env in available_environments:
            environment_names.append([env.split('/')[-1].split('.')[0], env])
        return environment_names
      
    def _deploy(self):
        import sys

        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
        from foundations.global_state import config_manager     

        driver_name =   self._arguments.driver_file
        env_name = self._arguments.env
        env_file_path = EnvironmentFetcher().find_environment(env_name)

        if self._check_environment_valid(env_file_path, env_name) and self._check_driver_valid(driver_name):
            config_manager.add_simple_config_path(env_file_path[0])
            self._run_driver_file(driver_name)
        else:
            sys.exit(1)
    
    def _run_driver_file(self, driver_name):
        import os
        import sys
        from importlib import import_module
        
        driver_name, path_to_add = self._get_driver_and_path(driver_name)
        sys.path.append(path_to_add)
        os.chdir(path_to_add)
        import_module(driver_name)
               
    def _get_driver_and_path(self, driver_name):
        import os
        dirname = os.path.dirname(driver_name)

        if dirname:
            driver_name = os.path.basename(driver_name)
            path = os.path.join(os.getcwd(), dirname)
        else:
            path = os.getcwd()

        driver_name = driver_name.split('.')[0]               
        return driver_name, path
    
    def _check_environment_valid(self, environment_file_path, environment_name):
        valid = False
        if environment_file_path == None:
            print("Foundations project not found. Deploy command must be run in foundations project directory")
        elif len(environment_file_path) == 0:
            print("Could not find environment name: `{}`. You can list all discoverable environments with `foundations info --env`".format(environment_name))
        else:
            valid = True
        return valid
    
    def _check_driver_valid(self, driver_name):
        import os
        if not os.path.isfile(os.path.join(os.getcwd(), driver_name)):
            print('Driver file `{}` does not exist'.format(driver_name))
            return False
        if driver_name.split('.')[-1] != 'py':
            print('Driver file `{}` needs to be a python file with an extension `.py`'.format(driver_name))
            return False
        return True 
