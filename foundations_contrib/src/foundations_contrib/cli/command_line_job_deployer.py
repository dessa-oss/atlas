"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CommandLineJobDeployer(object):

    def __init__(self, arguments):
        self._entrypoint = arguments.entrypoint
        self._env = arguments.env if arguments.env is not None else 'local'
        self._job_directory = arguments.job_directory
        self._project_name = arguments.project_name
        self._ram = arguments.ram
        self._num_gpus = arguments.num_gpus

    def deploy(self):
        import os
        import sys

        import foundations
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
        from foundations_contrib.global_state import config_manager
        
        if self._job_directory is not None:
            os.chdir(self._job_directory)

        env_file_path = EnvironmentFetcher().find_environment(self._env)

        if self._check_environment_valid(env_file_path):
            config_manager.add_simple_config_path(env_file_path[0])
        else:
            sys.exit(1)

        if self._stages_enabled():
            self._deploy_job_with_stages()
        else:
            self._check_and_set_job_resources()
            deploy_kwargs = self._stageless_deploy_kwargs()
            deployment_wrapper = foundations.deploy(**deploy_kwargs)
            self._with_clean_exit(self._stream_logs_if_possible, deployment_wrapper)

    def _check_environment_valid(self, environment_file_path):
        valid = False
        if environment_file_path == None:
            print("Foundations project not found. Deploy command must be run in foundations project directory")
        elif len(environment_file_path) == 0:
            print("Could not find environment name: `{}`. You can list all discoverable environments with `foundations info --env`\n\nExpected usage of deploy command: `usage: foundations deploy [-h] [--env ENV] driver_file`".format(self._env))
        else:
            valid = True
        return valid

    def _stages_enabled(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['run_script_environment'].get('enable_stages', False)

    def _check_and_set_job_resources(self):
        import foundations

        set_resources_args = {}

        if self._ram is not None:
            set_resources_args['ram'] = self._ram

        if self._num_gpus is not None:
            set_resources_args['num_gpus'] = self._num_gpus

        if set_resources_args:
            foundations.set_job_resources(**set_resources_args)

    def _stageless_deploy_kwargs(self):
        entrypoint = self._entrypoint
        env_name = self._env
        project_name = self._project_name
        job_directory = self._job_directory

        deploy_kwargs = {}

        if project_name is not None:
            deploy_kwargs['project_name'] = project_name

        deploy_kwargs['env'] = env_name if env_name is not None else 'local'

        if entrypoint is not None:
            deploy_kwargs['entrypoint'] = entrypoint

        return deploy_kwargs

    def _with_clean_exit(self, callback, *callback_args, **callback_kwargs):
        try:
            return callback(*callback_args, **callback_kwargs)
        except KeyboardInterrupt:
            return

    def _stream_logs_if_possible(self, deployment_wrapper):
        from foundations_contrib.global_state import log_manager

        foundations_cli_logger = log_manager.get_logger(__name__)

        log_stream = self._get_log_stream(deployment_wrapper)

        if self._log_streaming_is_enabled() and log_stream is not None:
            foundations_cli_logger.info('Job is queued; Ctrl-C to stop streaming - job will not be interrupted or cancelled')                    
            is_running = False

            for log_line in log_stream:
                if not is_running:
                    is_running = True
                    foundations_cli_logger.info('Job is running; streaming logs')

                print(log_line, flush=True)

    def _deploy_job_with_stages(self):
        import sys

        self._set_project_name()

        driver_name = self._entrypoint

        if self._check_driver_valid(driver_name):
            self._check_and_set_job_resources()

            driver_name, path_to_add = self._get_driver_and_path(driver_name)
            self._set_up_working_dir_for_job_with_stages(path_to_add)
            self._run_module(driver_name)
        else:
            sys.exit(1)

    def _get_log_stream(self, deployment_wrapper):
        try:
            return deployment_wrapper.stream_job_logs()
        except NotImplementedError:
            return None

    def _log_streaming_is_enabled(self):
        import os
        return os.environ.get('DISABLE_LOG_STREAMING', 'False') == 'False'

    def _set_project_name(self):
        from foundations_contrib.global_state import current_foundations_context

        if self._project_name:
            project_name = self._project_name
        else:
            project_name = 'default'

        current_foundations_context().set_project_name(project_name)

    def _check_driver_valid(self, driver_name):
        import os
        if not os.path.isfile(os.path.join(os.getcwd(), driver_name)):
            print('Driver file `{}` does not exist'.format(driver_name))
            return False
        if driver_name.split('.')[-1] != 'py':
            print('Driver file `{}` needs to be a python file with an extension `.py`'.format(driver_name))
            return False
        return True

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

    def _set_up_working_dir_for_job_with_stages(self, working_dir):
        import os
        import sys

        os.chdir(working_dir)
        sys.path.append(working_dir)

    def _run_module(self, module_name):
        from importlib import import_module
        import_module(module_name)