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