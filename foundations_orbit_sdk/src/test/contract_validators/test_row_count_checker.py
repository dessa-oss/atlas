
from foundations_spec import *

from foundations_orbit.contract_validators.row_count_checker import RowCountChecker

class TestRowCountChecker(Spec):

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def row_count(self):
        return self.faker.random_number()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)

    @let_now
    def dataframe_one_row(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]])

    @let_now
    def dataframe_two_rows(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]]*2)

    @let_now
    def dataframe_four_rows(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]]*4)

    def test_row_count_difference_is_zero_if_both_row_counts_are_equal(self):
        checker = RowCountChecker(1)
        expected_result = {
            'expected_row_count': 1,
            'actual_row_count': 1,
            'row_count_diff': 0.0
        }
        self.assertEqual(expected_result, checker.validate(self.dataframe_one_row))

    def test_row_count_difference_is_100_percent_if_current_row_count_is_twice_the_reference(self):
        checker = RowCountChecker(1)
        expected_result = {
            'expected_row_count': 1,
            'actual_row_count': 2,
            'row_count_diff': 1.0
        }
        self.assertEqual(expected_result, checker.validate(self.dataframe_two_rows))

    def test_row_count_difference_is_300_percent_if_current_row_count_is_four_times_the_reference(self):
        checker = RowCountChecker(1)
        expected_result = {
            'expected_row_count': 1,
            'actual_row_count': 4,
            'row_count_diff': 3.0
        }
        self.assertEqual(expected_result, checker.validate(self.dataframe_four_rows))

    def test_row_count_difference_is_50_percent_if_current_row_count_is_half_the_reference(self):
        checker = RowCountChecker(2)
        expected_result = {
            'expected_row_count': 2,
            'actual_row_count': 1,
            'row_count_diff': -0.5
        }
        self.assertEqual(expected_result, checker.validate(self.dataframe_one_row))

    def test_string_cast_for_row_count_checker_returns_expected_information(self):
        import json
        checker = RowCountChecker(self.row_count)

        expected_information = {
            'number_of_rows': self.row_count
        }
        self.assertEqual(json.dumps(expected_information), str(checker))

    def test_row_count_checker_can_accept_configurations(self):
        checker = RowCountChecker(self.row_count)
        self.assertIsNotNone(getattr(checker, "configure", None))
        
    def test_row_count_checker_can_accept_exclusions(self):
        checker = RowCountChecker(self.row_count)
        self.assertIsNotNone(getattr(checker, "exclude", None))

    def test_row_count_checker_is_zero_if_configured_with_correct_row_number(self):
        checker = RowCountChecker(1)
        checker.configure(row_count = 2)
        expected_result = {
            'expected_row_count': 2,
            'actual_row_count': 2,
            'row_count_diff': 0.0
        }
        self.assertEqual(expected_result, checker.validate(self.dataframe_two_rows))
    
    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)