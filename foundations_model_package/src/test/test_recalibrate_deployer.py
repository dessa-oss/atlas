"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import time

class TestRecalibrateDeployer(Spec):

    mock_orbit_deployer = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.deploy_without_uploading')
    mock_get_latest_for_job = let_patch_mock('foundations_scheduler.pod_fetcher.get_latest_for_job')
    mock_time = let_patch_mock('time.sleep')
    mock_time.return_value = None

    @let
    def project_name(self):
        return self.faker.word()
    
    @let
    def model_name(self):
        return self.faker.word()

    @let
    def project_directory(self):
        return self.faker.uri_path()

    @let
    def job_id(self):
        return self.faker.uuid4()
    @let
    def message(self):
        return {'job_id': self.job_id}

    def test_calls_orbit_serve_start_with_correct_params(self):
        from foundations_model_package.recalibrate_deployer import RecalibrateDeployer
        
        retrain_deployer = RecalibrateDeployer(job_id=self.job_id, project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory)
        retrain_deployer.start()

        self.mock_orbit_deployer.assert_called_with(project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory, job_id=self.job_id ,env='scheduler')

    def test_job_status_when_given_job_id_returns_pending_get_latest_for_job_returns_none(self):
        from foundations_model_package.recalibrate_deployer import _job_status

        self.mock_get_latest_for_job.return_value = None
        self.assertEqual('Pending', _job_status(self.job_id))

    def test_job_status_when_given_job_id_returns_pending_get_latest_for_job_returns_pod_with_pending_status(self):
        from foundations_model_package.recalibrate_deployer import _job_status

        mock_pod = Mock()
        mock_pod.status.phase = 'Pending'
        self.mock_get_latest_for_job.return_value = mock_pod

        self.assertEqual('Pending', _job_status(self.job_id))

    def test_job_status_when_given_job_id_returns_running_get_latest_for_job_returns_pod_with_running_status(self):
        from foundations_model_package.recalibrate_deployer import _job_status

        mock_pod = Mock()
        mock_pod.status.phase = 'Running'
        self.mock_get_latest_for_job.return_value = mock_pod

        self.assertEqual('Running', _job_status(self.job_id))

    def test_wait_for_statuses_does_calls_job_status_once_if_job_status_not_in_status_list(self):
        from foundations_model_package.recalibrate_deployer import _wait_for_statuses

        mock_job_status = self.patch('foundations_model_package.recalibrate_deployer._job_status', ConditionalReturn())
        mock_job_status.return_when('Completed', self.job_id)
        _wait_for_statuses(self.job_id, ['Pending', 'Running'], '')

        mock_job_status.assert_called_once()

    def test_wait_for_statuses_raises_assertion_error_with_correct_message_if_job_times_out(self):
        from foundations_model_package.recalibrate_deployer import _wait_for_statuses

        mock_job_status = self.patch('foundations_model_package.recalibrate_deployer._job_status', ConditionalReturn())
        mock_job_status.return_when('Pending', self.job_id)
        error_message = 'some error message'

        with self.assertRaises(AssertionError) as ex:
            _wait_for_statuses(self.job_id, ['Pending', 'Running'], error_message)

        self.assertEqual(error_message, str(ex.exception))

    def test_wait_for_complete_job_calls_wait_for_statuses_with_right_arguments(self):
        from foundations_model_package.recalibrate_deployer import _wait_for_job_to_complete

        mock_wait_for_statuses = self.patch('foundations_model_package.recalibrate_deployer._wait_for_statuses')
        _wait_for_job_to_complete(self.job_id)
        mock_wait_for_statuses.assert_called_with(self.job_id, ['Pending', 'Running'], 'job did not finish')






    