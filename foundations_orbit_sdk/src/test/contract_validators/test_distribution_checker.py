"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.contract_validators.distribution_checker import DistributionChecker

class TestDistributionChecker(Spec):

    @let
    def default_distribution_options(self):
        return {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

    @let
    def checker_with_one_column_df(self):
        return DistributionChecker(self.default_distribution_options, [self.column_name], self.bin_stats, self.one_column_dataframe)

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    @let
    def bin_stats(self):
        return {}

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)

    @let_now
    def one_column_dataframe(self):
        import numpy
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let_now
    def two_column_dataframe_no_rows(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)

    def test_distribution_checker_cannot_validate_if_checking_distribution_if_both_column_whitelist_and_column_blacklist_are_set(self):
        options = self.default_distribution_options.copy()
        options['cols_to_ignore'] = []
        options['cols_to_include'] = []

        checker = DistributionChecker(options, [self.column_name], {}, self.one_column_dataframe)

        with self.assertRaises(ValueError) as ex:
            checker.distribution_check_results()

        self.assertIn('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes', ex.exception.args)

    def test_distribution_check_empty_dataframe_against_itself_returns_empty_dist_check_results(self):
        distribution_checker = DistributionChecker(self.default_distribution_options, [], None, None)
        self.assertEqual({}, distribution_checker.distribution_check_results())

    def test_distribution_check_single_column_dataframe_against_itself_returns_dist_check_result_with_one_entry(self):
        import numpy

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            }
        }
        distribution_checker = DistributionChecker(self.default_distribution_options, [self.column_name], None, None)
        self.assertEqual(expected_dist_check_result, distribution_checker.distribution_check_results())

    def test_distribution_check_multiple_column_dataframe_against_itself_returns_dist_check_result_with_multiple_entries(self):
        import numpy

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            },
            self.column_name_2: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            }
        }

        distribution_checker = DistributionChecker(self.default_distribution_options, [self.column_name, self.column_name_2], None, None)
        self.assertEqual(expected_dist_check_result, distribution_checker.distribution_check_results())