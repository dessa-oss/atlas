"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.data_contract_options import DataContractOptions

class TestDataContractOptions(Spec):

    @let
    def random_int(self):
        return self.faker.random.randint(0, 100)

    @let
    def random_int_2(self):
        return self.faker.random.randint(0, 100)

    @let
    def random_int_3(self):
        return self.faker.random.randint(0, 100)

    @let
    def random_int_4(self):
        return self.faker.random.randint(0, 100)

    def test_data_contract_options_has_max_bins(self):
        self._test_data_contract_options_has_attribute('max_bins')

    def test_data_contract_options_has_check_schema(self):
        self._test_data_contract_options_has_attribute('check_schema')

    def test_data_contract_options_has_check_row_count(self):
        self._test_data_contract_options_has_attribute('check_row_count')
    
    def test_data_contract_options_has_special_values(self):
        self._test_data_contract_options_has_attribute('special_values')

    def test_data_contract_options_has_check_distribution(self):
        self._test_data_contract_options_has_attribute('check_distribution')
    
    def test_data_contract_options_has_distribution_check(self):
        self._test_data_contract_options_has_attribute('distribution')

    def test_data_contract_options_are_equal_if_special_values_consists_of_a_numpy_nan_and_was_loaded_from_pickle(self):
        import numpy
        import pickle

        options = DataContractOptions(special_values=[numpy.nan])
        other_options = DataContractOptions(special_values=[numpy.nan])

        self.assertEqual(options, pickle.loads(pickle.dumps(other_options)))

    def test_data_contract_options_are_not_equal_if_special_values_are_not_equal(self):
        options = DataContractOptions(special_values=[self.random_int])
        other_options = DataContractOptions(special_values=[1])

        self.assertNotEqual(options, other_options)

    def test_data_contract_options_nan_is_not_equal_to_random_int(self):
        import numpy
        
        options = DataContractOptions(special_values=[numpy.nan])
        other_options = DataContractOptions(special_values=[self.random_int])

        self.assertNotEqual(options, other_options)

    def test_data_contract_options_are_equal_if_special_values_are_equal_and_not_nan(self):
        options = DataContractOptions(special_values=[self.random_int])
        other_options = DataContractOptions(special_values=[self.random_int])

        self.assertEqual(options, other_options)

    def test_data_contract_options_are_not_equal_if_special_values_are_not_equal_multiple_values(self):
        options = DataContractOptions(special_values=[self.random_int, self.random_int_2])
        other_options = DataContractOptions(special_values=[self.random_int, self.random_int_3])

        self.assertNotEqual(options, other_options)

    def _test_data_contract_options_has_attribute(self, attribute_name):
        attribute_value = Mock()

        options = DataContractOptions(**{attribute_name: attribute_value})
        self.assertEqual(attribute_value, getattr(options, attribute_name))