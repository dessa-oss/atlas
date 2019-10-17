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
        pause_parser.set_defaults(function=self._pause_monitor)

    
    def _pause_monitor(self):
        pass