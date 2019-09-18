"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy
import pandas
from foundations_spec import *

from foundations_orbit.contract_validators.distribution_checker import DistributionChecker

class TestDistributionChecker(Spec):

    @let
    def distribution_options(self):
        return {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

    @let
    def checker_with_one_column_df(self):
        return DistributionChecker(self.distribution_options, [self.column_name], self.bin_stats, self.one_column_dataframe)

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    @let
    def bin_stats(self):
        return {
            self.column_name: [{
                'value':  numpy.nan,
		        'percentage': 0.0
            },
            {
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }],
            self.column_name_2: [{
                'value':  numpy.nan,
		        'percentage': 0.0
            },
            {
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }

    @let
    def bin_stats_one_column_no_special_value(self):
        return {
            self.column_name: [{
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)


    @let_now
    def one_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let_now
    def two_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[5,6],[10,32]], dtype=numpy.int8)

    @let_now
    def two_column_dataframe_no_rows(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)

    def test_distribution_checker_cannot_validate_if_checking_distribution_if_both_column_whitelist_and_column_blacklist_are_set(self):
        options = self.distribution_options.copy()
        options['cols_to_ignore'] = []
        options['cols_to_include'] = []

        checker = DistributionChecker(options, [self.column_name], self.bin_stats, self.one_column_dataframe)

        with self.assertRaises(ValueError) as ex:
            checker.distribution_check_results()

        self.assertIn('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes', ex.exception.args)

    def test_distribution_check_empty_dataframe_against_itself_returns_empty_dist_check_results(self):
        distribution_checker = DistributionChecker(self.distribution_options, [], self.bin_stats, None)
        self.assertEqual({}, distribution_checker.distribution_check_results())

    def test_distribution_check_single_column_dataframe_against_itself_returns_dist_check_result_with_one_entry(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
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
        distribution_checker = DistributionChecker(self.distribution_options, [self.column_name], self.bin_stats, self.one_column_dataframe)
        self.assertEqual(expected_dist_check_result, distribution_checker.distribution_check_results())

    def test_distribution_check_multiple_column_dataframe_against_itself_returns_dist_check_result_with_multiple_entries(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
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
                'binned_l_infinity': 1.0,
                'binned_passed': False,
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

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.bin_stats, self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, checker.distribution_check_results())

    def test_distribution_check_single_column_dataframe_for_non_special_values_in_bin(self):
        self.maxDiff = None
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
                'special_values': {}
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name], self.bin_stats_one_column_no_special_value, self.one_column_dataframe)
        self.assertEqual(expected_dist_check_result, checker.distribution_check_results())

    def test_distribution_check_one_column_dataframe_with_upper_edge(self):
        bin_stats = {
             self.column_name: [{
                'value': 1,
                'percentage': 1.0,
                'upper_edge': 20
            }]
        }
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
                'special_values': {}
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name], bin_stats, self.one_column_dataframe)
        self.assertEqual(expected_dist_check_result, checker.distribution_check_results())


    def test_distribution_check_two_column_dataframe_with_both_containing_upper_edges(self):
        self.maxDiff = None
        bin_stats = {
             self.column_name: [{
                'value': 1,
                'percentage': 0.5,
                'upper_edge': 20
            }],
            self.column_name_2: [{
                'value': 1,
                'percentage': 0.5,
                'upper_edge': 20
            }]
        }
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {}
            },
            self.column_name_2: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {}
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], bin_stats, self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, checker.distribution_check_results())

    @skip('need to confirm behaviour with MLE ... behaviour of apply edges causes test to break')
    def test_distribution_check_two_column_dataframe_with_upper_edge_and_non_special_values_in_bin(self):
        bin_stats = {
            self.column_name: [{
                'value': 1,
                'percentage': 0.5,
                'upper_edge': 20
            },{
                'value': 2,
                'percentage': 0.5,
                'upper_edge': 20
            }],
            self.column_name_2: [{
                'value': 1,
                'percentage': 0.6,
                'upper_edge': 20
            },{
                'value': 2,
                'percentage': 0.4,
                'upper_edge': 20
            }]
        }

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
                'special_values': {}
            },
            self.column_name_2: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
                'special_values': {}
            }
        }


        checker = DistributionChecker(self.distribution_options, [self.column_name], bin_stats, self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, checker.distribution_check_results())
