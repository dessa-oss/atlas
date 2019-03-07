"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest

from mock import Mock

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
