"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker

class TestMinMax(Spec):

    @let
    def column_name(self):
        return self.faker.word()

    @let_now
    def dataframe_one_column(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name], data=[20, 40, 50, 100, 110])

    def test_min_max_test_returns_empty_dictionary_when_checker_not_configured(self):
        min_max_checker = MinMaxChecker()
        result = min_max_checker.validate(self.dataframe_one_column)
        self.assertEqual({}, result)
    
    def test_min_max_test_raises_value_error_if_bounds_not_passed_and_attributes_empty(self):
        min_max_checker = MinMaxChecker()

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=[])

    def test_min_max_test_raises_value_error_if_bounds_not_passed(self):
        min_max_checker = MinMaxChecker()

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=['abc'])
    
    def test_min_max_test_passes_when_lower_bound_provided(self):
        lower_bound = self.faker.random.randint(0, self.dataframe_one_column[self.column_name].min() - 1)
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': 20
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_fails_when_lower_bound_provided_greater_than_min_value(self):
        lower_bound = 30
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': False,
                    'min_value': 20,
                    'percentage_out_of_bounds': 0.2
                }
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_passes_when_upper_bound_provided(self):
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()
        upper_bound = self.faker.random.randint(max_val_of_dataframe + 1, max_val_of_dataframe + 100)
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_of_dataframe
                }
            }
        }

        self.assertEqual(expected_result, result)

    
    def test_min_max_test_returns_empty_dict_with_empty_dataframe(self):
        import pandas

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=self.faker.random.randint(0,10))
        result = min_max_checker.validate(pandas.DataFrame())

        expected_result = {}

        self.assertEqual(expected_result, result)
