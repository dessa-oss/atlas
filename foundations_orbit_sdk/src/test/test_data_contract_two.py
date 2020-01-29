"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import fakeredis
from foundations_orbit.data_contract import DataContract
from foundations_spec import *

# Created new class for testing data contract
class TestDataContractTwo(Spec):

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    def _two_column_dataframe(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]])

    @set_up
    def set_up(self):
        self.project_name = self.faker.word()
        self.model_name = self.faker.word()
        self.contract_name = self.faker.word()
        self.inference_period = '2019-07-06'
        self.column_name = self.faker.word()
        self.column_name_2 = self.faker.word()

        mock_environ = self.patch('os.environ', {})
        mock_environ['PROJECT_NAME'] = self.project_name
        mock_environ['MONITOR_NAME'] = self.model_name

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_data_contract_has_options_with_default_check_domain_True(self):
        self._test_data_contract_has_default_option('check_domain', True)

    def test_data_contract_has_domain_checker(self):
        self._test_data_contract_has_test_as_attribute('domain_test')

    def test_data_contract_has_options_with_default_check_uniqueness_True(self):
        self._test_data_contract_has_default_option('check_uniqueness', True)

    def test_data_contract_has_uniqueness_checker(self):
        self._test_data_contract_has_test_as_attribute('uniqueness_test')

    def test_data_contract_has_domain_checker_configured(self):
        from foundations_orbit.contract_validators.domain_checker import DomainChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('domain_test', DomainChecker)

    def test_data_contract_has_uniqueness_checker_configured(self):
        from foundations_orbit.contract_validators.uniqueness_checker import UniquenessChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('uniqueness_test', UniquenessChecker)

    def test_data_contract_domain_check_produces_correct_output_for_two_column_df(self):
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self._two_column_dataframe())
        contract.domain_test.configure(attributes=[self.column_name])
        report = contract.validate(self._two_column_dataframe(), inference_period=inference_period)

        self.assertIn('domain_test_results', report)
    
    def test_data_contract_uniqueness_check_produces_correct_output_for_two_column_df(self):
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self._two_column_dataframe())
        contract.uniqueness_test.configure(attributes=[self.column_name])
        report = contract.validate(self._two_column_dataframe(), inference_period=inference_period)

        self.assertIn('uniqueness_test_results', report)

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertEqual(default_value, getattr(contract.options, option_name))

    def _test_data_contract_has_test_as_attribute(self, test_name):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertIsNotNone(getattr(contract, test_name, None))

    def _test_data_contract_has_test_which_is_an_instance_of_expected_class(self, test_name, class_type):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertIsInstance(getattr(contract, test_name, None), class_type)