
from foundations_spec import *
from foundations_orbit.contract_validators.checker import Checker

class TestChecker(Spec):
    
    @let
    def column_name_one(self):
        return self.faker.word()


    @let
    def column_name_two(self):
        return self.faker.word()

    @let
    def column_name_three(self):
        return self.faker.word()
    @let
    def allowed_data_types_min_max(self):
        return ['int', 'float', 'datetime']

    @let
    def reference_column_types_int(self):
        return {self.column_name_one: 'int'}

    @let
    def reference_column_types_bool(self):
        return {self.column_name_one: 'bool'}
    
    @let
    def reference_column_types_multiple(self):
        return {self.column_name_one: 'bool', self.column_name_two: 'int', self.column_name_three: 'float'}

    def test_checker_returns_empty_list_with_no_args(self):
        valid_attributes = Checker.find_invalid_attributes(allowed_column_types=[], reference_column_types={})
        self.assertEqual([], valid_attributes)

    def test_checker_returns_empty_list_when_reference_column_types_is_empty(self):
        valid_attributes_one = Checker.find_invalid_attributes(allowed_column_types=self.allowed_data_types_min_max, reference_column_types={})
        self.assertEqual([], valid_attributes_one)

    def test_checker_returns_one_attribute_when_no_allowed_columns(self):
        valid_attributes_two = Checker.find_invalid_attributes(allowed_column_types=[], reference_column_types=self.reference_column_types_int)
        self.assertEqual([self.column_name_one], valid_attributes_two)

    def test_checker_returns_empty_list_when_allowed_column_matches_with_reference_types(self):
        valid_attributes = Checker.find_invalid_attributes(allowed_column_types=[self.allowed_data_types_min_max[0]], reference_column_types=self.reference_column_types_int)
        self.assertEqual([], valid_attributes)        

    def test_checker_returns_corresponding_column_name_when_allowed_column_does_not_match_with_reference_types(self):
        valid_attributes_one = Checker.find_invalid_attributes(allowed_column_types=[self.allowed_data_types_min_max[1]], reference_column_types=self.reference_column_types_int)
        valid_attributes_two = Checker.find_invalid_attributes(allowed_column_types=[self.allowed_data_types_min_max[0]], reference_column_types=self.reference_column_types_bool)
        self.assertEqual([self.column_name_one], valid_attributes_one)
        self.assertEqual([self.column_name_one], valid_attributes_two)

    def test_checker_returns_expected_list_when_some_reference_columns_match_allowed_columns(self):
        valid_attributes = Checker.find_invalid_attributes(allowed_column_types=self.allowed_data_types_min_max, reference_column_types=self.reference_column_types_multiple)
        self.assertEqual([self.column_name_one], valid_attributes)
