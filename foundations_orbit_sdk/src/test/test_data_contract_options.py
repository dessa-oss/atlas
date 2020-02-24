
from foundations_spec import *

from foundations_orbit.data_contract_options import DataContractOptions

class TestDataContractOptions(Spec):

    @let
    def random_int(self):
        return self.faker.random.randint(2, 100)

    @let
    def random_int_2(self):
        return self.faker.random.randint(101, 200)

    @let
    def random_int_3(self):
        return self.faker.random.randint(201, 300)

    @let
    def random_int_4(self):
        return self.faker.random.randint(301, 400)

    def test_data_contract_options_has_check_row_count(self):
        self._test_data_contract_options_has_attribute('check_row_count')
    
    def test_data_contract_options_has_check_distribution(self):
        self._test_data_contract_options_has_attribute('check_distribution')
    
    def test_data_contract_options_has_min_max_check(self):
        self._test_data_contract_options_has_attribute('check_min_max')

    
    def test_data_contract_options_has_domain_check(self):
        self._test_data_contract_options_has_attribute('check_domain')

    def test_data_contract_options_has_uniqueness_check(self):
        self._test_data_contract_options_has_attribute('check_uniqueness')

    def test_data_contract_options_equal_by_default(self):
        self.assertEqual(DataContractOptions(), DataContractOptions())

    def test_data_contract_not_equal_if_check_row_count_not_equal(self):
        options = DataContractOptions(check_row_count=False)
        other_options = DataContractOptions(check_row_count=True)

        self.assertNotEqual(options, other_options)

    def test_data_contract_not_equal_if_check_distribution_not_equal(self):
        options = DataContractOptions(check_distribution=False)
        other_options = DataContractOptions(check_distribution=True)

        self.assertNotEqual(options, other_options)


    def test_data_contract_not_equal_if_check_special_values_is_set(self):
        options = DataContractOptions(check_special_values=True)
        other_options = DataContractOptions()

        self.assertNotEqual(options, other_options)


    def _test_data_contract_options_has_attribute(self, attribute_name):
        attribute_value = Mock()

        options = DataContractOptions(**{attribute_name: attribute_value})
        self.assertEqual(attribute_value, getattr(options, attribute_name))