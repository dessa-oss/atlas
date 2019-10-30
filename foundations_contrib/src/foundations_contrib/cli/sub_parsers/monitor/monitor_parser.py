"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MonitorParser(object):
    
    def __init__(self, commandline):
        self._cli = commandline

    def add_sub_parser(self):
        from argparse import REMAINDER
        
        monitor_help = 'Provides operations for managing monitors in Orbit'
        monitor_parser = self._cli.add_sub_parser('monitor', help=monitor_help)
        monitor_sub_parser = monitor_parser.add_subparsers()

        pause_parser = monitor_sub_parser.add_parser('pause')
        pause_parser.add_argument('project_name', type=str, help='Project containing monitor to pause')
        pause_parser.add_argument('name', type=str, help='Name of monitor to pause')
        pause_parser.add_argument('--env', type=str, required=False, metavar='', help='Specifies the scheduler environment (Default: `scheduler`)')
        pause_parser.set_defaults(function=self._pause_monitor)

        start_parser = monitor_sub_parser.add_parser('create')
        start_parser.add_argument('--name', type=str, metavar='', help='Name of monitor to create (Default: name of command script')
        start_parser.add_argument('--project_name', type=str, metavar='', help='Project that the monitor will be created in (Default: current working directory)')
        start_parser.add_argument('--env', type=str, required=False, metavar='', help='Specifies the scheduler environment (Default: `scheduler`)')
        start_parser.add_argument('job_directory', type=str, help='Directory from which to create the monitor')
        start_parser.add_argument('command', type=str, nargs=REMAINDER, help='Monitor script to create')
        start_parser.set_defaults(function=self._start_monitor)

        delete_parser = monitor_sub_parser.add_parser('delete')
        delete_parser.add_argument('project_name', metavar='project_name', help='Project that the monitor will be deleted from')
        delete_parser.add_argument('name', type=str, metavar='name', help='Name of monitor to delete')
        delete_parser.add_argument('--env', type=str, required=False, metavar='', help='Specifies the scheduler environment (Default: `scheduler`)')
        delete_parser.set_defaults(function=self._delete_monitor)

        resume_parser = monitor_sub_parser.add_parser('resume')
        resume_parser.add_argument('project_name', type=str, help='Project containing monitor to resume')
        resume_parser.add_argument('name', type=str, help='Name of monitor to resume')
        resume_parser.add_argument('--env', type=str, required=False, metavar='', help='Specifies the scheduler environment (Default: `scheduler`)')
        resume_parser.set_defaults(function=self._resume_monitor)

    def _start_monitor(self):
        from requests.exceptions import ConnectionError
        from foundations_contrib.cli.orbit_monitor_package_server import start

        arguments = self._cli.arguments()
        job_directory = arguments.job_directory
        command = arguments.command
        project_name = arguments.project_name
        name = arguments.name
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'
        
        name, project_name = self._get_name_and_project_name_for_error(name, project_name, command)

        try:
            start(job_directory, command, project_name, name, env)
            print(f'Successfully created monitor {name} in project {project_name}')
        except ValueError as ex:
            import sys

            print(f'Unable to create monitor {name} in project {project_name}')
            sys.exit(f'Command failed with error: {str(ex)}')
        except ConnectionError as ex:
            import sys

            print(f'Unable to create monitor {name} in project {project_name}')
            sys.exit('Command failed with error: Could not connect to docker scheduler')

    def _get_name_and_project_name_for_error(self, name, project_name, command):
        from os import path, getcwd

        if name is None:
            name = command[0].replace('.', '-')
        if project_name is None:
            project_name = path.basename(getcwd())

        return name, project_name

    def _modify_monitor(self, monitor_modifier_func):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError
        
        monitor_name = self._cli.arguments().name
        project_name = self._cli.arguments().project_name
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'

        try:
            monitor_modifier_func(project_name, monitor_name, env)
            print(f'Successfully {str(monitor_modifier_func.__name__)}d monitor {monitor_name} from project {project_name}')
        except CronJobSchedulerError as ce:
            import sys
            print(f'Unable to {str(monitor_modifier_func.__name__)} monitor {monitor_name} from project {project_name}')
            sys.exit(f'Command failed with error: {str(ce)}')
    
    def _delete_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import delete
        self._modify_monitor(delete)

    def _pause_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause
        self._modify_monitor(pause)

    def _resume_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import resume
        self._modify_monitor(resume)
