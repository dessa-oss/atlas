"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.data_contract_summary import DataContractSummary


class TestDataContractSummary(Spec):

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

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
    def att(self):
        return self.faker.word()

    @staticmethod
    def _key_to_write(project_name, monitor_package, data_contract):
        return f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}:summary'

    def _write_summary_to_redis(self, project_name, monitor_package, data_contract, inference_period, summary):
        import pickle

        key_to_write = self._key_to_write(project_name, monitor_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, pickle.dumps(summary))

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_validation_report_get_returns_none_if_report_not_in_redis(self):
        promise = DataContractSummary.get(
            self.project_name, self.monitor_package, self.data_contract, self.inference_period, self.att)
        self.assertIsNone(promise.evaluate())

    def test_validation_report_get_returns_report_if_report_in_redis(self):
        attribute_summary = {
            'expected_data_summary': {
                'percentage_missing': 0.5,
                'minimum': 1,
                'maximum': 100
            },
            'actual_data_summary': {
                'percentage_missing': 0.33,
                'minimum': 10,
                'maximum': 25021421
            },
            'binned_data': {
                'bins': ['a', 'b', 'c'],
                'data': {
                    'expected_data': [1, 2, 3],
                    'actual_data': [4, 5, 6]
                }
            }
        }

        total_summary = {
            'attribute_summaries': {
                self.att: attribute_summary
            },
            'num_critical_tests': 3
        }

        self._write_summary_to_redis(
            self.project_name, self.monitor_package, self.data_contract, self.inference_period, total_summary)

        promise = DataContractSummary.get(
            self.project_name, self.monitor_package, self.data_contract, self.inference_period, self.att)

        self.assertEqual(attribute_summary, promise.evaluate())
