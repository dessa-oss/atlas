"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy
import pandas
from foundations_spec import *

from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker

class TestSpecialValuesChecker(Spec):

    @let
    def distribution_options(self):
        return {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()


    @let_now
    def one_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

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
    def bin_stats_two_columns_with_special_values(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': None
            }, {
                'value':  numpy.nan,
		        'percentage': 0.0
            }],
            self.column_name_2: [{
                'value':  numpy.nan,
		        'percentage': 0.0
            },{
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
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

    @let_now
    def two_column_dataframe_no_rows(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)
    
    def test_schema_checker_can_accept_configurations(self):
        checker = SpecialValuesChecker({}, None, None)
        self.assertIsNotNone(getattr(checker, "configure", None))
        
    def test_schema_checker_can_accept_exclusions(self):
        checker = SpecialValuesChecker({}, None, None)
        self.assertIsNotNone(getattr(checker, "exclude", None))

    def test_special_values_check_for_mulitple_column_df_against_itself_returns_all_passed_using_not_previously_defined_special_value(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
        data = {
            self.column_name: [5, 10, 15, -1],
            self.column_name_2: [6, 32, 40, -1]
        }

        dataframe = pandas.DataFrame(data)
        special_values = [-1]

        bin_stats = {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name])),
            self.column_name_2: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name_2]))
        }


        expected_check_results = {
            self.column_name:{
                -1: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }, 
            self.column_name_2:{
                -1: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker = SpecialValuesChecker(self.distribution_options, bin_stats, [self.column_name, self.column_name_2])
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={ -1: 0.1 })
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def _create_two_column_bin_stats_from_data(self, data, special_character):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats

        special_values = [special_character]

        return {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name])),
            self.column_name_2: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name_2]))
        }

    def _create_two_column_data_and_dataframe_with_special_characeters(self, special_character):
        data = {
            self.column_name: [5, 10, 15, special_character],
            self.column_name_2: [6, 32, 40, special_character]
        }

        dataframe = pandas.DataFrame(data)
        return data, dataframe

    def _create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(self, special_character):
        data, dataframe = self._create_two_column_data_and_dataframe_with_special_characeters(special_character)
        bin_stats = self._create_two_column_bin_stats_from_data(data, special_character)
        return SpecialValuesChecker(self.distribution_options, bin_stats, [self.column_name, self.column_name_2]), dataframe
    
    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed_for_configured_column(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1})

        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed_excluding_column(self):
        expected_check_results = {
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})

        checker.exclude(attributes=[self.column_name])
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)
    
    def test_special_values_checker_allows_exclude_all(self):
        expected_check_results = {}

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)


    def test_special_values_check_configure_multiple_times_appends_to_previous_configurations(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1 })
        checker.configure(attributes=[self.column_name_2], thresholds={numpy.nan: 0.1 })
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_requires_attributes_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure()
            self.fail('Failed to throw appropraite error message for missing attribute')
        except ValueError as ve:
            self.assertTrue('attribute is required' in str(ve).lower())

    def test_special_values_check_requires_threshold_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure(attributes=[])
            self.fail('Failed to throw appropraite error message for missing attribute')
        except ValueError as ve:
            self.assertTrue('threshold is required' in str(ve).lower())

    def test_special_values_check_requires_threshold_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure(attributes=[], thresholds=[])
            self.fail('Failed to throw appropraite error message for incorrectly specified threshold')
        except ValueError as ve:
            self.assertTrue('invalid threshold' in str(ve).lower())

    def test_special_values_check_configure_uses_values_in_thresholds_to_determine_if_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.5,
                    'passed': False
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.5,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={ numpy.nan: 0.1 })
        checker.configure(attributes=[self.column_name_2], thresholds={ numpy.nan: 0.5 })
        
        dataframe_to_validate = dataframe.copy()
        dataframe_to_validate.iloc[-2,:2] = numpy.nan

        results = checker.validate(dataframe_to_validate)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_configure_applies_values_in_thresholds_to_all_specified_columns_to_determine_if_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={ numpy.nan: 0.1 })
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)