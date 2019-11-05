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
            'custom_thresholds': {},
            'custom_methods': {},
        }

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()


    @let_now
    def one_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let_now
    def one_column_dataframe_reference_types(self):
        return {self.column_name: 'int'}
    @let
    def bin_stats_one_column(self):
        return {
            self.column_name: [{
                'value': 4,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }
    
    @let_now
    def two_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[5,6],[10,32]], dtype=numpy.int8)
    
    @let_now
    def two_column_dataframe_reference_types(self):
        return {self.column_name: 'int8', self.column_name_2: 'int8'}

    @let
    def bin_stats_two_column_no_special_value(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': 10
            },  {'percentage': 0.0, 'upper_edge': numpy.inf}],
            self.column_name_2: [{
		        'percentage': 1.0,
                'upper_edge': 32
            },  {'percentage': 0.0, 'upper_edge': numpy.inf}]
        }

    @let
    def bin_stats_two_column_no_special_value_no_zeros(self):
        return {
            self.column_name: [{
                'percentage': 0.8,
                'upper_edge': 10
            },  {'percentage': 0.2, 'upper_edge': numpy.inf}],
            self.column_name_2: [{
		        'percentage': 0.6,
                'upper_edge': 32
            },  {'percentage': 0.4, 'upper_edge': numpy.inf}]
        }

    @let
    def bin_stats(self):
        return {
            self.column_name: [{
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

    @let
    def categorical_attributes_one_numerical_column(self):
        return {self.column_name:False}
    
    @let
    def categorical_attributes_two_numerical_columns(self):
        return {self.column_name:False, self.column_name_2:False}
        
    @let_now
    def two_column_dataframe_no_rows(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)

    def test_string_cast_for_distribution_checker_returns_expected_information(self):
        import json

        checker = DistributionChecker(self.distribution_options, [self.column_name], reference_column_types={self.column_name: 'int'}, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker.set_bin_stats(self.bin_stats)

        expected_information = {
            'distribution_options': self.distribution_options,
            'bin_stats': self.bin_stats,
            'reference_column_names': [self.column_name],
            'reference_column_types': {
                self.column_name: 'int'
            }
        }

        self.assertEqual(str(expected_information), str(checker))

    def test_distribution_checker_cannot_validate_if_checking_distribution_if_both_column_whitelist_and_column_blacklist_are_set(self):
        options = self.distribution_options.copy()
        options['cols_to_ignore'] = []
        options['cols_to_include'] = []

        checker = DistributionChecker(options, [self.column_name], reference_column_types=self.one_column_dataframe_reference_types,categorical_attributes=self.categorical_attributes_one_numerical_column)

        with self.assertRaises(ValueError) as ex:
            checker.validate(self.one_column_dataframe)

        self.assertIn('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes', ex.exception.args)

    def test_distribution_check_throws_error_if_dataframe_is_none_when_validate_called(self):
        with self.assertRaises(ValueError) as ex:
            DistributionChecker(self.distribution_options, [], {}, categorical_attributes={}).validate(None)

    def test_distribution_check_throws_error_if_dataframe_is_empty_when_validate_called(self):
        with self.assertRaises(ValueError) as ex:
            checker = DistributionChecker(self.distribution_options, [], {}, {})
            checker.validate(self.empty_dataframe)

    def test_distribution_check_single_column_dataframe_against_itself_returns_dist_check_result_with_one_entry(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            }
        }
        distribution_checker = DistributionChecker(self.distribution_options, [self.column_name], self.one_column_dataframe_reference_types,categorical_attributes=self.categorical_attributes_one_numerical_column)
        distribution_checker.set_bin_stats(self.bin_stats_one_column)
        self.assertEqual(expected_dist_check_result, distribution_checker.validate(self.one_column_dataframe))

    def test_distribution_check_multiple_column_dataframe_against_itself_returns_dist_check_result_with_multiple_entries(self):
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }, 
            self.column_name_2: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }}

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_check_single_column_dataframe_for_non_special_values_in_bin(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker.set_bin_stats(self.bin_stats_one_column_no_special_value)
        self.assertEqual(expected_dist_check_result, checker.validate(self.one_column_dataframe))

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
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker.set_bin_stats(bin_stats)
        self.assertEqual(expected_dist_check_result, checker.validate(self.one_column_dataframe))

    def test_distribution_check_with_large_value_ranges(self):
        data = {
            self.column_name: [100,25,46],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
            },
            self.column_name_2: {
                'binned_l_infinity':  0.667,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)
        validate_results = checker.validate(dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)

    def test_multiple_column_dataframe_will_only_produce_results_for_columns_specified_in_configure(self):
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }}

        checker = DistributionChecker(self.distribution_options, self.bin_stats_two_column_no_special_value, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes = [self.column_name])
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)

    def test_multiple_column_dataframe_will_only_produce_results_for_columns_specified_in_configure(self):
        
        expected_dist_check_result = {
            self.column_name_2: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }}

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes = [self.column_name])
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_run_with_all_columns_excluded_returns_empty_dictionary(self):

        expected_dist_check_result = {}
    
        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_uses_defaults_when_run(self):

        data = {
            self.column_name: [1,2,3,4,5,6,7,8,9,1.5,100],
            self.column_name_2: [50,2,400,51,52,53,54,55,56,57,58]
        }
        dataframe = pandas.DataFrame(data)
        

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.091,
                'binned_passed': 0.091 < checker._distribution_options['default_threshold'],
            },
            self.column_name_2: {
                'binned_l_infinity':  0.909,
                'binned_passed': 0.909 < checker._distribution_options['default_threshold'],
            }
        }

        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)

        validate_results = checker.validate(dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_runs_test_on_all_column_names_that_are_configured(self):

        data = {
            self.column_name: [1,2,3],
            self.column_name_2: [4,5,6]
        }
        dataframe = pandas.DataFrame(data)
        
        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name])
        checker.configure(attributes=[self.column_name_2])
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)

        validate_results = checker.validate(dataframe)

        self.assertIn(self.column_name, validate_results)
        self.assertIn(self.column_name_2, validate_results)

    def test_distribution_checker_runs_test_on_all_column_names_that_are_configured_with_threshold(self):

        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.333,
                'binned_passed': False,
            },
            self.column_name_2: {
                'binned_l_infinity':  0.667,
                'binned_passed': True,
            }
        }
        
        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name])
        checker.configure(attributes=[self.column_name_2], threshold=0.7)
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_runs_test_as_expected_on_columns_configured_with_psi_method(self):
        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_psi':  0.093,
                'binned_passed': True,
            },
            self.column_name_2: {
                'binned_psi': 0.293,
                'binned_passed': False,
            }
        }
        
        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name, self.column_name_2], method='psi')
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value_no_zeros)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_runs_test_as_expected_on_columns_configured_with_different_methods(self):
        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.133,
                'binned_passed': False,
            },
            self.column_name_2: {
                'binned_psi': 0.293,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.configure(attributes=[self.column_name_2], method='psi')
        checker.set_bin_stats(self.bin_stats_two_column_no_special_value_no_zeros)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_configure_raises_value_error_when_unsupported_columns_used(self):
        reference_column_types = {self.column_name: 'int', self.column_name_2: 'object'}
        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], reference_column_types=reference_column_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name], threshold=0.1, method='l_infinity')

        expected_error_dictionary = {
            self.column_name_2: 'object'
        }

        with self.assertRaises(ValueError) as e:
            checker.configure(attributes=[self.column_name_2], threshold=0.1, method='l_infinity')

        self.assertEqual(f'The following columns have invalid types: {expected_error_dictionary}', e.exception.args[0])
    
    def test_distribution_checker_provides_expected_output_when_given_categorical_data(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical

        data = {
            self.column_name: [1,1,1,2,2,2],
            self.column_name_2: [1.0]*6
        }
        dataframe = pandas.DataFrame(data)
        categorical_attributes = {self.column_name:True, self.column_name_2:False}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(special_values=[], col_values=dataframe[self.column_name])
        bin_stats[self.column_name_2] = create_bin_stats(special_values=[], max_bins=10, col_values=dataframe[self.column_name_2])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.0,
                'binned_passed': True,
            },
            self.column_name_2: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
            }
        }

        checker = DistributionChecker(self.distribution_options, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.configure(attributes=[self.column_name_2], method='l_infinity')
        checker.set_bin_stats(bin_stats)
        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_provides_expected_output_when_given_categorical_data_and_using_l_infinity(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical
        import numpy

        data = {
            self.column_name: [1,1,1,2,2,2],
        }

        dataframe = pandas.DataFrame(data)
        categorical_attributes = {self.column_name:True}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(special_values=[], col_values=dataframe[self.column_name])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.333,
                'binned_passed': False,
            },
        }
        checker = DistributionChecker(self.distribution_options, [self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')

        dataframe.iloc[0,0] = self.faker.pyint()
        dataframe.iloc[1,0] = self.faker.pyint()

        checker.set_bin_stats(bin_stats)
        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_provides_expected_output_with_zeros_input(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical
        import numpy

        reference_data = {
            self.column_name: [0]*99 + [1],
        }

        reference_dataframe = pandas.DataFrame(reference_data)

        current_data = {
            
        }
        categorical_attributes = {self.column_name:True}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(special_values=[], col_values=reference_dataframe[self.column_name])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.0,
                'binned_passed': True,
            },
        }
        checker = DistributionChecker(self.distribution_options, [self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.set_bin_stats(bin_stats)

        validate_results = checker.validate(reference_dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)