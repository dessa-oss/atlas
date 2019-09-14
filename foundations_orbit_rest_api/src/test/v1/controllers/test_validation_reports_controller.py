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
    def num_rows(self):
        return self.faker.random.randint(1, 1000)

    @let
    def controller(self):
        return ValidationReportsController()

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

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

    def test_post_returns_200_as_response_if_report_in_redis(self):
        expected_response_data = {
            'schema_check': True,
            'schema_information': {
                'rows': self.num_rows
            }
        }

        self._register_report(self.project_name, self.model_package, self.data_contract, self.inference_period, expected_response_data)
        response = self.controller.post()

        self.assertEqual(200, response.status())

    def test_post_returns_report_if_report_in_redis(self):
        expected_response_data = {
            'schema_check': True,
            'schema_information': {
                'rows': self.num_rows
            }
        }

        self._register_report(self.project_name, self.model_package, self.data_contract, self.inference_period, expected_response_data)
        response = self.controller.post()

        self.assertEqual(expected_response_data, response.as_json())

    @staticmethod
    def _key_to_write(project_name, model_package, data_contract):
        return f'projects:{project_name}:models:{model_package}:validation:{data_contract}'

    def _register_report(self, project_name, model_package, data_contract, inference_period, validation_report):
        import pickle

        key_to_write = self._key_to_write(project_name, model_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, pickle.dumps(validation_report))