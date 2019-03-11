"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest

from mock import Mock, patch

from foundations_internal.testing.helpers import set_up, tear_down
from foundations_internal.testing.helpers.spec import Spec
from foundations.deployment_wrapper import DeploymentWrapper

class TestDeploymentWrapper(Spec):

    def test_job_name_returns_deployment_job_name(self):
        deployment = Mock()
        deployment.job_name.return_value = 'job1'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.job_name(), 'job1')
    
    def test_job_name_returns_deployment_job_name_different_name(self):
        deployment = Mock()
        deployment.job_name.return_value = 'job2'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.job_name(), 'job2')

    def test_is_job_complete_returns_true_if_deployment_job_is_complete(self):
        deployment = Mock()
        deployment.is_job_complete.return_value = True

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertTrue(deployment_wrapper.is_job_complete())
    
    def test_is_job_complete_returns_false_if_deployment_job_is_not_complete(self):
        deployment = Mock()
        deployment.is_job_complete.return_value = False

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertFalse(deployment_wrapper.is_job_complete())
    
    def test_get_job_status_returns_completed_if_deployment_job_is_completed(self):
        deployment = Mock()
        deployment.get_job_status.return_value = 'Completed'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.get_job_status(),'Completed')
    
    def test_get_job_status_returns_completed_if_deployment_job_is_queued(self):
        deployment = Mock()
        deployment.get_job_status.return_value = 'Queued'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.get_job_status(),'Queued')

    @patch('time.sleep')
    def test_wait_for_deployment_to_complete_only_sleeps_if_job_not_complete(self, mock_time_sleep):
        deployment = Mock()
        states = [False, True]
        deployment.job_name.return_value = 'whatever'
        deployment.is_job_complete = lambda: states.pop(0)

        deployment_wrapper = DeploymentWrapper(deployment)
        deployment_wrapper.wait_for_deployment_to_complete()
        mock_time_sleep.assert_called_once_with(5)
    
    @patch('time.sleep')
    def test_wait_for_deployment_to_complete_only_sleeps_for_specified_time_if_job_not_complete(self, mock_time_sleep):
        deployment = Mock()
        states = [False, True]
        deployment.job_name.return_value = 'whatever'
        deployment.is_job_complete = lambda: states.pop(0)

        deployment_wrapper = DeploymentWrapper(deployment)
        deployment_wrapper.wait_for_deployment_to_complete(2)
        mock_time_sleep.assert_called_once_with(2)

    @patch('foundations_internal.remote_exception.check_result')
    def test_fetch_job_results_calls_check_results_with_correct_arguments(self, check_result_mock):
        deployment = Mock()
        deployment.fetch_job_results.return_value = 'result'
        deployment.job_name.return_value = 'whatever'
        deployment.is_job_complete.return_value = True

        deployment_wrapper = DeploymentWrapper(deployment)
        deployment_wrapper.fetch_job_results()

        check_result_mock.assert_called_once_with('whatever', 'result')
    
    @patch('foundations_internal.remote_exception.check_result')
    def test_fetch_job_results_returns_check_result_return_value(self, check_result_mock):
        deployment = Mock()
        deployment.fetch_job_results.return_value = 'result'
        deployment.job_name.return_value = 'whatever'
        deployment.is_job_complete.return_value = True

        check_result_mock.return_value = 'Result is checked'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.fetch_job_results(), 'Result is checked')


    def test_get_job_logs_returns_deployment_object_get_job_logs_return_value(self):
        deployment = Mock()
        deployment.get_job_logs.return_value = 'some fancy logs'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.get_job_logs(), 'some fancy logs')
    
    def test_get_job_logs_returns_deployment_object_get_job_logs_different_return_value(self):
        deployment = Mock()
        deployment.get_job_logs.return_value = 'some fancier logs'

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.get_job_logs(), 'some fancier logs')
    
    def test_get_job_logs_returns_error_message_if_deployment_object_does_not_have_get_job_logs_method(self):
        deployment = object()

        deployment_wrapper = DeploymentWrapper(deployment)
        self.assertEqual(deployment_wrapper.get_job_logs(), 'Current deployment method does not support get_job_logs()')