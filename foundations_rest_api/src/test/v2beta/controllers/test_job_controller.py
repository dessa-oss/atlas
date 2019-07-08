"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v2beta.models.property_model import PropertyModel

from foundations_spec import *

class TestJobControllerV2(Spec):

    mock_cancel_job = let_patch_mock('foundations_contrib.jobs.kubernetes_job.cancel')

    @let
    def controller(self):
        from foundations_rest_api.v2beta.controllers.job_controller import JobController
        return JobController()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        self.controller.job_id = self.job_id

    def test_cancels_running_job(self):
        self.controller.delete()
        self.mock_cancel_job.assert_called_with(self.job_id)

    def test_returns_a_confirmation_message(self):
        expected_result = f'Job {self.job_id} successfull cancelled'
        self.assertEqual(expected_result, self.controller.delete().as_json())
