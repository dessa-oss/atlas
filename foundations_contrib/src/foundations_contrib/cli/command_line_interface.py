"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CommandLineInterface(object):
    
    def __init__(self, args):
        from argparse import ArgumentParser

        self._argument_parser = ArgumentParser(prog='foundations')
        self._argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        self._argument_parser.set_defaults(function=self._no_command)
        subparsers = self._argument_parser.add_subparsers()
        
        init_parser = subparsers.add_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)
        
        self._arguments = self._argument_parser.parse_args(args)

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
            print('Success: New Foundations project {} created!'.format(project_name))
        else:
            print('Error: project directory for {} already exists'.format(project_name))
