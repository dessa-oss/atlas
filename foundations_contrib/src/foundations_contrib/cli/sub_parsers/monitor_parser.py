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
        monitor_help = 'Provides operations for managing monitors in Orbit'
        monitor_parser = self._cli.add_sub_parser('monitor', help=monitor_help)
        monitor_sub_parser = monitor_parser.add_subparsers()

        pause_parser = monitor_sub_parser.add_parser('pause')
        pause_parser.add_argument('monitor_name', type=str)
        pause_parser.add_argument('project_name', type=str)
        pause_parser.set_defaults(function=self._pause_monitor)

    
    def _pause_monitor(self):
        from foundations_contrib.global_state import config_manager
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler, CronJobSchedulerError
        
        monitor_name = self._cli.arguments().monitor_name
        project_name = self._cli.arguments().project_name
        monitor_id = f'{project_name}-{monitor_name}'

        try:
            CronJobScheduler(config_manager.config()['scheduler_url']).pause_job(monitor_id)
        except CronJobSchedulerError as ce:
            import sys
            sys.exit(str(ce))
