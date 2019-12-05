"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import ValidationReportListingsController

class TestValidationReportListingsController(Spec):

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_package(self):
        return self.faker.word()

    @let
    def data_contract(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @let
    def num_critical_tests(self):
        return self.faker.random_number()

    @let
    def monitor_package_2(self):
        return self.faker.word()

    @let
    def data_contract_2(self):
        return self.faker.word()

    @let
    def inference_period_2(self):
        return self.faker.date()

    @let
    def num_critical_tests2(self):
        return self.faker.random_number()

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def controller(self):
        return ValidationReportListingsController()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()
        self.controller.params = {'project_name': self.project_name}

    def test_index_returns_empty_list_as_response_if_no_reports_in_redis(self):
        self.assertEqual([], self.controller.index().as_json())

    def test_index_returns_resource_with_resource_name_validation_report_listings(self):
        result = self.controller.index()
        self.assertEqual('ValidationReportListings', result.resource_name())

    def test_index_returns_list_with_one_listing_if_exists_in_redis(self):
        self._register_report(self.project_name, self.monitor_package, self.data_contract, self.inference_period, self.num_critical_tests)
        result = self.controller.index()

        expected_result = [
            {
                'data_contract': self.data_contract,
                'monitor_package': self.monitor_package,
                'inference_period': self.inference_period,
                'num_critical_tests': self.num_critical_tests
            }
        ]

        self.assertEqual(expected_result, result.as_json())

    def test_index_returns_list_with_all_listings_is_sorted_by_inference_period(self):
        self._register_report(self.project_name, self.monitor_package, self.data_contract, '2019-10-13', self.num_critical_tests)
        self._register_report(self.project_name, self.monitor_package_2, self.data_contract_2, '2019-03-04', self.num_critical_tests2)
        result = self.controller.index()

        expected_result = [
            {
                'data_contract': self.data_contract_2,
                'monitor_package': self.monitor_package_2,
                'inference_period': '2019-03-04',
                'num_critical_tests': self.num_critical_tests2
            },
            {
                'data_contract': self.data_contract,
                'monitor_package': self.monitor_package,
                'inference_period': '2019-10-13',
                'num_critical_tests': self.num_critical_tests
            }
        ]

        self.assertEqual(expected_result, result.as_json())

    # TODO: This test randomly failed at one point
    def test_index_returns_list_with_all_listings_is_sorted_by_inference_period_followed_by_monitor_package(self):
        self._register_report(self.project_name, 'dog_bark', self.data_contract_2, '2019-10-13', self.num_critical_tests2)
        self._register_report(self.project_name, 'cat_meow', self.data_contract, '2019-10-13', self.num_critical_tests)
        result = self.controller.index()

        expected_result = [
            {
                'data_contract': self.data_contract,
                'monitor_package': 'cat_meow',
                'inference_period': '2019-10-13',
                'num_critical_tests': self.num_critical_tests
            },
            {
                'data_contract': self.data_contract_2,
                'monitor_package': 'dog_bark',
                'inference_period': '2019-10-13',
                'num_critical_tests': self.num_critical_tests2
            }
        ]

        self.assertEqual(expected_result, result.as_json())

    def test_index_returns_list_with_all_listings_is_sorted_by_inference_period_followed_by_monitor_package_followed_by_data_contract(self):
        self._register_report(self.project_name, 'cat_meow', 'data_contract_2', '2019-10-13', self.num_critical_tests2)
        self._register_report(self.project_name, 'cat_meow', 'data_contract', '2019-10-13', self.num_critical_tests)
        result = self.controller.index()

        expected_result = [
            {
                'data_contract': 'data_contract',
                'monitor_package': 'cat_meow',
                'inference_period': '2019-10-13',
                'num_critical_tests': self.num_critical_tests
            },
            {
                'data_contract': 'data_contract_2',
                'monitor_package': 'cat_meow',
                'inference_period': '2019-10-13',
                'num_critical_tests': self.num_critical_tests2
            }
        ]

        self.assertEqual(expected_result, result.as_json())
        
    @staticmethod
    def _key_to_write(project_name, monitor_package, data_contract):
        return f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}', \
               f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}:summary'

    def _register_report(self, project_name, monitor_package, data_contract, inference_period, num_critical_tests):
        import pickle
        key_to_write, summary_key_to_write = self._key_to_write(project_name, monitor_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, 'dummy_report')
        data_contract_summary = {
            'num_critical_tests': num_critical_tests
        }
        self.redis_connection.hset(summary_key_to_write, inference_period, pickle.dumps(data_contract_summary))