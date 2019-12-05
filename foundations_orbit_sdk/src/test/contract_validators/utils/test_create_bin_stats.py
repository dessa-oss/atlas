"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical
import pandas as pd
import numpy as np

class TestCreateBinStats(Spec):

    def test_creates_bin_for_empty_series(self):
        max_bins = 10
        col_values = pd.Series([])
        with self.assertRaises(ValueError) as value_error:
            create_bin_stats(max_bins, col_values)

    def test_creates_bin_ignores_nan_in_column(self):
        max_bins = 10
        col_values = pd.Series([1, np.nan])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_has_mulitple_of_the_same_unique_value(self):
        max_bins = 10
        col_values = pd.Series([1,1,1,1,1])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_ignores_infinite_value(self):
        max_bins = 10
        col_values = pd.Series([1, np.inf])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_no_special_values(self):
        max_bins = 10
        col_values = pd.Series([1, 2])

        expected_output = [{
            'percentage': 0.5,
            'upper_edge': 1.5
        }, {
            'percentage': 0.5,
            'upper_edge': np.inf
        }]

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_create_bin_for_columns_with_negative_max_bin(self):
        max_bins = -1
        col_values = pd.Series([1, 21])

        with self.assertRaises(ValueError) as value_error:
            create_bin_stats(max_bins, col_values)


    def test_create_bin_for_columns_with_max_bin_as_float(self):
        special_values = []
        max_bins = 0.5
        col_values = pd.Series([1, 21])

        try:
            create_bin_stats(max_bins, col_values)
        except ValueError as value_error:
            self.assertTrue('must be defined as an integer' in str(value_error).lower())

    def test_create_bin_for_columns_with_unique_values_greater_than_max_bin(self):
        special_values = []
        max_bins = 2
        col_values = pd.Series([1,2,3,4])

        expected_output = [{
            'percentage': 0.5,
            'upper_edge': 2.5
        }, {
            'percentage': 0.5,
            'upper_edge': np.inf
        }]

        output = create_bin_stats(max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_create_bin_stats_categorical_returns_empty_dict_when_empty_arguments_passed(self):
        import numpy, pandas
        result = create_bin_stats_categorical(col_values=pandas.Series([]), min_category_threshold=0)

        self.assertEqual(result, [])
    
    def test_create_bin_stats_categorical_returns_expected_output_with_single_value_input(self):
        import numpy, pandas
        single_value_series = pandas.Series([1]*100)
        result = create_bin_stats_categorical(col_values=single_value_series, min_category_threshold=0)

        expected_result = [
            {
                'category_value':1,
                'percentage':1.0
            },
            {
                'other_bins':True,
                'percentage':0
            }
        ]
        self.assertEqual(result, expected_result)

    def test_create_bin_stats_categorical_returns_expected_output_with_multiple_cateogry_input(self):
        import pandas
        single_value_series = pandas.Series([1]*20 +  [2]*30 + [3]*30 + [4]*20)
        result = create_bin_stats_categorical(col_values=single_value_series, min_category_threshold=0)

        expected_result = [

            {
                'category_value':1,
                'percentage':0.2
            },
            {
                'category_value':2,
                'percentage':0.3
            },
            {
                'category_value':3,
                'percentage':0.3
            },
            {
                'category_value':4,
                'percentage':0.2
            },
            {
                'other_bins':True,
                'percentage':0
            }
        ]

        self.assertEqual(result, expected_result)

    def test_create_bin_stats_categorical_returns_expected_output_with_multiple_cateogry_input_and_multiple_special_values(self):
        import pandas
        single_value_series = pandas.Series([1]*20 +  [2]*30)
        result = create_bin_stats_categorical(col_values=single_value_series, min_category_threshold=0)

        expected_result = [
            {
                'category_value':1,
                'percentage':0.4
            },
            {
                'category_value':2,
                'percentage':0.6
            },
            {
                'other_bins':True,
                'percentage':0
            }
        ]

        self.assertEqual(result, expected_result)

    def test_create_bin_stats_categorical_returns_expected_output_with_multiple_cateogry_input_and_min_treshold(self):
        import pandas
        single_value_series = pandas.Series([1]*50 +  [2]*30 + [4]*10 + [5]*10)
        result = create_bin_stats_categorical(col_values=single_value_series, min_category_threshold=0.12)

        expected_result = [
            {
                'category_value':1,
                'percentage':0.5
            },
            {
                'category_value':2,
                'percentage':0.3
            },
            {
                'other_bins':True,
                'percentage':0.2
            }
        ]

        self.assertEqual(result, expected_result)