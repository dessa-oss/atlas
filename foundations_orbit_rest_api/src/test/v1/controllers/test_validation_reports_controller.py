"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import ValidationReportsController

class TestValidationReportsController(Spec):

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_package(self):
        return self.faker.word()

    @let
    def data_contract(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @let
    def controller(self):
        return ValidationReportsController()

    @set_up
    def set_up(self):
        self.controller.params = {
            'project_name': self.project_name,
            'inference_period': self.inference_period,
            'model_package': self.model_package,
            'data_contract': self.data_contract
        }

    def test_post_returns_404_as_response_if_report_not_in_redis(self):
        response = self.controller.post()
        self.assertEqual(404, response.status())

    def test_post_returns_data_with_error_message_if_report_not_in_redis(self):
        response = self.controller.post()
        expected_response_data = {
            'inference_period': self.inference_period,
            'model_package': self.model_package,
            'data_contract': self.data_contract,
            'error': 'does not exist'
        }

        self.assertEqual(expected_response_data, response.as_json())