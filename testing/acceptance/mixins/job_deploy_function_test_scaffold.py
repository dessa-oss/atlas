"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from acceptance.mixins.metrics_fetcher import MetricsFetcher

class JobDeployFunctionTestScaffold(MetricsFetcher):

    @property
    def foundations_global_configs_directory(self):
        import os.path as path
        return path.expanduser('~/.foundations/config')

    @property
    def local_config_file_path(self):
        import os.path as path
        return path.expanduser('~/.foundations/config/local.config.yaml')

    @property
    def local_config_file_contents(self):
        return {
            'job_deployment_env': 'local',
            'results_config': {},
            'cache_config': {},
            'obfuscate_foundations': False,
            'log_level': self._log_level()
        }

    @property
    def job_directory(self):
        return '/tmp/deploy_job_test'

    @property
    def project_directory(self):
        return 'acceptance/fixtures/deploy_job_via_function_project'

    @property
    def project_directory_default_entrypoint(self):
        return 'acceptance/fixtures/deploy_job_via_function_project_default_entrypoint'

    @property
    def entrypoint(self):
        return 'entrypoint.py'

    @property
    def environment(self):
        return 'an_environment'

    @property
    def project_name(self):
        return 'this-project'

    @property
    def expected_metrics(self):
        return {
            'learning_rate': 0.125,
            'layer_0_neuron': 5,
            'layer_1_neuron': 6
        }

    @property
    def deployment_parameters(self):
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

        if not path.isfile(self.local_config_file_path):
            self._should_remove_local_config_file_on_cleanup = True

            with open(self.local_config_file_path, 'w') as local_config_file:
                yaml.dump(self.local_config_file_contents, local_config_file)
        else:
            print('local config file already exists - will not remove')
            self._should_remove_local_config_file_on_cleanup = False

    def _tear_down(self):
        import os

        import foundations
        from acceptance.config import config

        if self._should_remove_local_config_file_on_cleanup:
            os.remove(self.local_config_file_path)

        foundations.config_manager.config().clear()
        foundations.config_manager.config().update(self._config_manager_body)

    def _test_deploy_job_with_all_arguments_specified_deploys_job(self):
        import os
        import os.path as path
        import shutil
        import yaml

        shutil.rmtree(self.job_directory, ignore_errors=True)
        shutil.copytree(self.project_directory, self.job_directory)

        environment_config_file_path = path.join(self.foundations_global_configs_directory, '{}.config.yaml'.format(self.environment))

        with open(environment_config_file_path, 'w') as environment_config_file:
            yaml.dump(self.local_config_file_contents, environment_config_file)

        job_uuid_container = self._deploy_job(
            job_directory=self.job_directory,
            entrypoint=self.entrypoint,
            project_name=self.project_name,
            env=self.environment,
            params=self.deployment_parameters
        )

        for metric_name, expected_metric_value in self.expected_metrics.items():
            self.assertEqual(expected_metric_value, self._get_logged_metric(self.project_name, self._uuid(job_uuid_container), metric_name))

        os.remove(environment_config_file_path)

    def _test_deploy_job_with_no_arguments_specified_deploys_job_with_defaults(self):
        import os
        import shutil

        shutil.rmtree(self.job_directory, ignore_errors=True)
        shutil.copytree(self.project_directory_default_entrypoint, self.job_directory)

        old_cwd = os.getcwd()

        os.chdir(self.job_directory)
        job_uuid_container = self._deploy_job_with_defaults()
        os.chdir(old_cwd)

        for metric_name, expected_metric_value in self.expected_metrics.items():
            self.assertEqual(expected_metric_value, self._get_logged_metric('deploy_job_test', self._uuid(job_uuid_container), metric_name))