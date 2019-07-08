"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

from foundations_scheduler_plugin.job_deployment import JobDeployment

class TestJobDeployment(Spec):

    mock_api_wrapper = let_patch_instance('foundations_scheduler_core.kubernetes_api_wrapper.KubernetesApiWrapper')
    mock_foundations_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')
    mock_filterwarnings = let_patch_mock('warnings.filterwarnings')

    @set_up
    def set_up(self):
        self.mock_foundations_context.job_resources.return_value = self.job_resources

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
        klass.return_when(instance, self.mock_api_wrapper, self.result_config)
        return instance

    @let
    def result_config(self):
        config = {'_is_deployment': True}
        config.update(self.config_manager_config)
        return config

    @let
    def config_manager_config(self):
        config = {'run_script_environment': {}}
        config.update(self.faker.pydict())
        return config

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

    @let
    def job_status(self):
        return self.faker.word()

    @let_now
    def mock_scheduler_job_status(self):
        self.mock_scheduler_instance.get_job_status = ConditionalReturn()
        self.mock_scheduler_instance.get_job_status.return_when(self.job_status, self.job_id)

    @let
    def job_logs(self):
        return self.faker.sentence()

    @let_now
    def mock_scheduler_job_logs(self):
        self.mock_scheduler_instance.get_job_logs = ConditionalReturn()
        self.mock_scheduler_instance.get_job_logs.return_when(self.job_logs, self.job_id)

    job = let_mock()
    job_source_bundle = let_mock()
    job_resources = let_mock()

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
        self.mock_scheduler_instance.submit_job.assert_called_with(self.job_id, self.path_to_tar, job_resources=self.job_resources)

    def test_get_job_status_returns_status(self):
        self.assertEqual(self.job_status, self.deployment.get_job_status())

    def test_get_job_logs_returns_logs(self):
        self.assertEqual(self.job_logs, self.deployment.get_job_logs())

    def test_is_job_complete_returns_false_when_not_completed(self):
        self.assertEqual(False, self.deployment.is_job_complete())

    def test_is_job_complete_returns_true_when_completed(self):
        self.mock_scheduler_instance.get_job_status = ConditionalReturn()
        self.mock_scheduler_instance.get_job_status.return_when('completed', self.job_id)

        self.assertEqual(True, self.deployment.is_job_complete())

    def test_get_job_status_returns_none_if_job_does_not_exist(self):
        from kubernetes.client.rest import ApiException

        self.mock_scheduler_instance.get_job_status.side_effect = ApiException(status=404)
        self.assertEqual(None, self.deployment.get_job_status())

    def test_get_job_status_reraises_exception_if_not_404(self):
        from kubernetes.client.rest import ApiException

        self.mock_scheduler_instance.get_job_status.side_effect = ApiException(status=400)

        with self.assertRaises(ApiException) as error_context:
            self.deployment.get_job_status()

        self.assertEqual(400, error_context.exception.status)

    def test_crypto_warning_should_not_be_printed(self):
        from cryptography.utils import CryptographyDeprecationWarning

        self.deployment.deploy()
        self.mock_filterwarnings.assert_called_with('ignore', category=CryptographyDeprecationWarning)

    def test_stream_job_logs_gets_stream_from_scheduler_object(self):
        mock_log_stream = Mock()
        self.mock_scheduler_instance.stream_job_logs = ConditionalReturn()
        self.mock_scheduler_instance.stream_job_logs.return_when(mock_log_stream, self.job_id)

        self.assertEqual(mock_log_stream, self.deployment.stream_job_logs())

    @staticmethod
    def _error_callback():
        raise Exception