"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import fakeredis
from foundations_orbit.data_contract import DataContract
from foundations_spec import *

class TestDataContractTwo(Spec):
    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    @set_up
    def set_up(self):
        self.project_name = self.faker.word()
        self.model_name = self.faker.word()
        self.contract_name = self.faker.word()

        mock_environ = self.patch('os.environ', {})
        mock_environ['PROJECT_NAME'] = self.project_name
        mock_environ['MONITOR_NAME'] = self.model_name

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_data_contract_has_options_with_default_check_distribution_True(self):
        self._test_data_contract_has_default_option('check_domain', True)

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertEqual(default_value, getattr(contract.options, option_name))