"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import abc
from subprocess import CompletedProcess
from foundations_spec import *

from acceptance.mixins.metrics_fetcher import MetricsFetcher
class JobDeployFunctionTestScaffold(abc.ABC, MetricsFetcher):
    
    @abc.abstractmethod
    def _submit_job_with_defaults(self) -> CompletedProcess:
        """Deploy a job using defaults and return the process."""

    @abc.abstractmethod
    def _submit_job(self, job_directory: str, entrypoint: str, project_name: str, env: str, params: dict) -> CompletedProcess:
        """Deploy a job and return the process."""

    @abc.abstractmethod
    def _uuid(self, driver_process: CompletedProcess) -> str:
        """Extract the uuid from a submited job."""

    @abc.abstractmethod
    def _log_level(self) -> str:
        """Return the log level."""

    @let
    def temp_home(self):
        import tempfile
        return tempfile.mkdtemp()

    @property
    def foundations_global_configs_directory(self):
        import os.path as path

        return self.temp_home + '/config/execution'

    @property
    def foundations_submission_config_directory(self):
        import os.path as path

        return self.temp_home + '/config/submission'

    @property
    def execution_config_file_path(self):
        import os.path as path

        return self.temp_home + '/config/execution/default.config.yaml'

    @property
    def scheduler_config_file_path(self):
        import os.path as path

        return self.temp_home + '/config/submission/scheduler.config.yaml'

    @property
    def execution_config_file_contents(self):
        return {
            'results_config': {},
            'cache_config': {},
            'obfuscate_foundations': False,
            'log_level': self._log_level()
        }

    @property
    def scheduler_config_file_contents(self):
        return {
            'results_config': {},
            'ssh_config': {},
        }

    @property
    def job_directory(self):
        return '/tmp/submit_job_test'

    @property
    def project_directory(self):
        return 'acceptance/fixtures/submit_job_via_function_project'

    @property
    def project_directory_default_entrypoint(self):
        return 'acceptance/fixtures/submit_job_via_function_project_default_entrypoint'

    @property
    def entrypoint(self):
        return 'entrypoint.py'

    @property
    def project_name(self):
        return 'this-project'

    @property
    def expected_metrics(self):
        return {
            'how_i_lern': 0.125,
            'first_boi': 5,
            'second_boi': 6
        }

    @property
    def submission_parameters(self):
        return {
            'learning_rate': 0.125,
            'layers': [
                {
                    'neurons': 5
                },
                {
                    'neurons': 6
                }
            ]
        }

    def _set_up(self):
        import os
        import os.path as path

        import yaml
        import copy

        import foundations
        from acceptance.cleanup import cleanup

        cleanup()

        self._config_manager_body = copy.deepcopy(foundations.config_manager.config())

        os.makedirs(self.foundations_global_configs_directory, exist_ok=True)
        os.makedirs(self.foundations_submission_config_directory, exist_ok=True)

        self._should_remove_config_files_on_cleanup = True

        with open(self.execution_config_file_path, 'w') as local_config_file:
            yaml.dump(self.execution_config_file_contents, local_config_file)

        with open(self.scheduler_config_file_path, 'w') as scheduler_config_file:
            yaml.dump(self.scheduler_config_file_contents, scheduler_config_file)

    def _tear_down(self):
        import os

        import foundations
        from acceptance.config import config

        if self._should_remove_config_files_on_cleanup:
            os.remove(self.execution_config_file_path)
            os.remove(self.scheduler_config_file_path)

        foundations.config_manager.config().clear()
        foundations.config_manager.config().update(self._config_manager_body)

    def _run_process(self, command):
        import subprocess
        import os

        environment = dict(os.environ)
        environment['FOUNDATIONS_HOME'] = self.temp_home

        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment)

    def _test_submit_job_with_all_arguments_specified_submits_job(self):
        import os
        import os.path as path
        import shutil
        import yaml

        shutil.rmtree(self.job_directory, ignore_errors=True)
        shutil.copytree(self.project_directory, self.job_directory)

        job_uuid_container = self._submit_job(
            job_directory=self.job_directory,
            entrypoint=self.entrypoint,
            project_name=self.project_name,
            params=self.submission_parameters
        )

        for metric_name, expected_metric_value in self.expected_metrics.items():
            self.assertEqual(expected_metric_value, self._get_logged_metric(self.project_name, self._uuid(job_uuid_container), metric_name))

    def _test_submit_job_with_no_arguments_specified_submits_job_with_defaults(self):
        import os
        import shutil
        from foundations_internal.change_directory import ChangeDirectory

        shutil.rmtree(self.job_directory, ignore_errors=True)
        shutil.copytree(self.project_directory_default_entrypoint, self.job_directory)

        with ChangeDirectory(self.job_directory):
            job_uuid_container = self._submit_job_with_defaults()

        for metric_name, expected_metric_value in self.expected_metrics.items():
            self.assertEqual(expected_metric_value, self._get_logged_metric('submit_job_test', self._uuid(job_uuid_container), metric_name))