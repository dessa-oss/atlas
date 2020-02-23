
from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import DataContractSummaryController

class TestDataContractSummaryController(Spec):

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

    @let
    def controller(self):
        return DataContractSummaryController()

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @staticmethod
    def _key_to_write(project_name, monitor_package, data_contract):
        return f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}:summary'

    def _write_summary_to_redis(self, project_name, monitor_package, data_contract, inference_period, summary):
        import pickle

        key_to_write = self._key_to_write(project_name, monitor_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, pickle.dumps(summary))

    @set_up
    def set_up(self):
        self.controller.params = {
            'project_name': self.project_name,
            'inference_period': self.inference_period,
            'monitor_package': self.monitor_package,
            'data_contract': self.data_contract
        }

    def test_index_returns_404_as_response_if_summary_not_in_redis(self):
        self.controller.params['attribute'] = 'this should not exist'
        response = self.controller.index()
        self.assertEqual(404, response.status())

    def test_index_returns_data_with_error_message_if_summary_not_in_redis(self):
        attribute = 'this should not exist'
        self.controller.params['attribute'] = attribute
        response = self.controller.index()
        expected_response_data = {
            'inference_period': self.inference_period,
            'monitor_package': self.monitor_package,
            'data_contract': self.data_contract,
            'project_name': self.project_name,
            'attribute': attribute,
            'error': 'does not exist'
        }

        self.assertEqual(expected_response_data, response.as_json())

    def test_index_returns_200_as_response_if_summary_in_redis(self):
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

        self.controller.params['attribute'] = self.att
        response = self.controller.index()

        self.assertEqual(200, response.status())

    def test_post_returns_report_if_report_in_redis(self):
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

        self.controller.params['attribute'] = self.att
        response = self.controller.index()

        self.assertEqual(attribute_summary, response.as_json())
