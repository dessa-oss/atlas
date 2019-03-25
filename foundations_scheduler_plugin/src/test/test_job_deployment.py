"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

from foundations_scheduler_plugin.job_deployment import JobDeployment

class TestJobDeployment(Spec):

    @let_now
    def mock_bundler_instance(self):
        instance = Mock()
        instance.job_archive.return_value = self.path_to_tar

        klass = self.patch('foundations_contrib.job_bundler.JobBundler', ConditionalReturn())
        klass.return_when(instance, self.job_id, self.result_config, self.job, self.job_source_bundle)
        return instance

    @let_now
    def mock_scheduler_instance(self):
        instance = Mock()
        klass = self.patch('foundations_scheduler.scheduler.Scheduler', ConditionalReturn())
        klass.return_when(instance, self.result_config)
        return instance

    @let
    def result_config(self):
        config = {'_is_deployment': True}
        config.update(self.config_manager_config)
        return config

    @let
    def config_manager_config(self):
        return self.faker.pydict()

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager.config().update(self.config_manager_config)
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @let
    def path_to_tar(self):
        return self.faker.uri_path()

    @let
    def deployment(self):
        return JobDeployment(self.job_id, self.job, self.job_source_bundle)

    @let
    def job_id(self):
        from uuid import uuid4
        return str(uuid4())

    job = let_mock()
    job_source_bundle = let_mock()

    def test_stores_config_with_manager_config(self):
        self.assertDictContainsSubset(
            self.config_manager_config,
            self.deployment.config()
        )

    def test_stores_config_with_deployment_mode_set(self):
        self.assertEqual(True, self.deployment.config()['_is_deployment'])

    def test_scheduler_method_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            JobDeployment.scheduler_backend()

    def test_job_name_is_job_id(self):
        self.assertEqual(self.job_id, self.deployment.job_name())

    def test_fetch_job_results_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.deployment.fetch_job_results()

    def test_deploy_bundles_job(self):
        self.deployment.deploy()
        self.mock_bundler_instance.bundle.assert_called()

    def test_deploy_cleans_up(self):
        self.deployment.deploy()
        self.mock_bundler_instance.cleanup.assert_called()

    def test_deploy_cleans_up_when_submit_fails(self):
        self.mock_scheduler_instance.submit_job.side_effect = self._error_callback

        try:
            self.deployment.deploy()
        except Exception:
            pass

        self.mock_bundler_instance.cleanup.assert_called()

    def test_deploy_submits_job_to_scheduler(self):
        self.deployment.deploy()
        self.mock_scheduler_instance.submit_job.assert_called_with(self.job_id, self.path_to_tar)

    @staticmethod
    def _error_callback():
        raise Exception