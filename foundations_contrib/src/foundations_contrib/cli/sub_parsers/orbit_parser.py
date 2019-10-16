"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class OrbitParser(object):

    def __init__(self, cli):
        self._cli = cli

    def add_sub_parser(self):
        help_msg = 'Provides operations for managing projects and models in Orbit'
        monitor_help = 'Provides operations for managing monitors in Orbit'
        orbit_parser = self._cli.add_sub_parser('orbit', help=help_msg)
        monitor_parser = self._cli.add_sub_parser('monitor', help=monitor_help)
        orbit_subparsers = orbit_parser.add_subparsers()
        self._add_serving_sub_parser(orbit_subparsers)

    def _add_serving_sub_parser(self, orbit_subparsers):
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
        serving_stop_parser.add_argument('--env', required=False, type=str, help='Specifies the execution environment where jobs are ran')
        serving_stop_parser.set_defaults(function=self._kubernetes_orbit_model_serving_stop)

        serving_destroy_parser = serving_subparsers.add_parser('destroy')
        serving_destroy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_destroy_parser.add_argument('--model_name', required=True, type=str, help='The unique name of the model within the project')
        serving_destroy_parser.add_argument('--env', required=False, type=str, help='Specifies the execution environment where jobs are ran')
        serving_destroy_parser.set_defaults(function=self._kubernetes_orbit_model_serving_destroy)

    def _broadcast_orbit_event(self, event, project_name, model_name, project_directory=None):
        from foundations_contrib.global_state import message_router
        message_router.push_message(event, {
            'project_name': project_name,
            'model_name':  model_name,
            'project_directory': project_directory
        })

    def _fail_with_message(self, message):
        import sys
        print(message)
        sys.exit(1)

    def _kubernetes_orbit_model_serving_deploy(self):
        from foundations_contrib.cli.orbit_model_package_server import deploy
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'local'
        try:
            project_name = self._cli.arguments().project_name
            model_name = self._cli.arguments().model_name
            project_directory = self._cli.arguments().project_directory
            successful = deploy(project_name, model_name, project_directory, env)
            if successful:
                self._broadcast_orbit_event('orbit_project_model_served', project_name, model_name, project_directory)
            else:
                message = f'Error: failed to serve model {model_name} in project {project_name}.'
                self._fail_with_message(message)
        except Exception as e:
            self._fail_with_message(e)

    def _kubernetes_orbit_model_serving_stop(self):
        from foundations_contrib.cli.orbit_model_package_server import stop
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'local'
        stop(self._cli.arguments().project_name, self._cli.arguments().model_name, env)

    def _kubernetes_orbit_model_serving_destroy(self):
        from foundations_contrib.cli.orbit_model_package_server import destroy
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'local'
        destroy(self._cli.arguments().project_name, self._cli.arguments().model_name, env)
