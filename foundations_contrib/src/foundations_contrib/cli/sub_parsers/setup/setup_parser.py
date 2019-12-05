"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SetupParser(object):

    def __init__(self, cli):
        self._cli = cli

    def add_sub_parser(self):
        setup_parser = self._cli.add_sub_parser('setup', help='Sets up Foundations for local experimentation')
        setup_subparsers = setup_parser.add_subparsers()
        setup_atlas_parser = setup_subparsers.add_parser('atlas')
        setup_orbit_parser = setup_subparsers.add_parser('orbit')
        
        setup_atlas_parser.set_defaults(function=self._run_atlas_setup)
        setup_orbit_parser.set_defaults(function=self._run_orbit_setup)

    def _run_atlas_setup(self):
        from subprocess import run
        import foundations_contrib

        run(['bash', './foundations_gui.sh', 'start', 'ui', 'foundations'], cwd=foundations_contrib.root() / 'resources')

    def _run_orbit_setup(self):
        from subprocess import run
        import foundations_contrib

        run(['bash', './foundations_gui.sh', 'start', 'ui', 'foundations-orbit'], cwd=foundations_contrib.root() / 'resources')

