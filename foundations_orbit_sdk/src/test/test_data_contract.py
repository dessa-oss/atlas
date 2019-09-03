"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.data_contract import DataContract

class TestDataContract(Spec):

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_file_for_write = let_mock()

    @let
    def contract_name(self):
        return self.faker.word()

    @let
    def model_package_directory(self):
        return self.faker.file_path()

    @let
    def data_contract_file_path(self):
        return f'{self.model_package_directory}/{self.contract_name}.pkl'

    @set_up
    def set_up(self):
        self.mock_file_for_write.__enter__ = lambda *args: self.mock_file_for_write
        self.mock_file_for_write.__exit__ = lambda *args: None

        self.mock_open.return_when(self.mock_file_for_write, self.data_contract_file_path, 'wb')

    def test_can_import_data_contract_from_foundations_orbit_top_level(self):
        import foundations_orbit
        self.assertEqual(DataContract, foundations_orbit.DataContract)

    def test_data_contract_takes_contract_name(self):
        try:
            DataContract(self.contract_name)
        except TypeError as ex:
            raise AssertionError('data contract class takes contract name as argument') from ex

    def test_data_contract_has_options_with_default_max_bins_50(self):
        self._test_data_contract_has_default_option('max_bins', 50)

    def test_data_contract_has_options_with_default_check_schema_True(self):
        self._test_data_contract_has_default_option('check_schema', True)

    def test_data_contract_has_options_with_default_check_row_count_False(self):
        self._test_data_contract_has_default_option('check_row_count', False)

    def test_data_contract_has_options_with_default_special_values_numpy_nan(self):
        import numpy
        self._test_data_contract_has_default_option('special_values', [numpy.nan])

    def test_data_contract_has_options_with_default_check_distribution_True(self):
        self._test_data_contract_has_default_option('check_distribution', True)

    def test_data_contract_has_distribution_option_distance_metric_with_default_value_l_infinity(self):
        self._test_distribution_check_has_default_option('distance_metric', 'l_infinity')

    def test_data_contract_has_distribution_option_default_threshold_0_1(self):
        self._test_distribution_check_has_default_option('default_threshold', 0.1)

    def test_data_contract_has_distribution_option_default_cols_to_include(self):
        self._test_distribution_check_has_default_option('cols_to_include', None)

    def test_data_contract_has_distribution_option_default_cols_to_ignore(self):
        self._test_distribution_check_has_default_option('cols_to_ignore', None)

    def test_data_contract_has_distribution_option_default_custom_thresholds(self):
        self._test_distribution_check_has_default_option('custom_thresholds', {})

    def test_data_contract_can_save_to_file(self):
        import pickle
        
        contract = DataContract(self.contract_name)
        contract.save(self.model_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def test_data_contract_preserves_options(self):
        import pickle
        
        contract = DataContract(self.contract_name)
        contract.options = {'asdf': 'value'}

        contract.save(self.model_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, getattr(contract.options, option_name))

    def _test_distribution_check_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, contract.options.distribution[option_name])