"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
import pandas as pd
import numpy as np

class TestCreateBinStats(Spec):

    def test_creates_bin_for_empty_series(self):
        special_values = []
        max_bins = 10
        col_values = pd.Series([])
        with self.assertRaises(ValueError) as value_error:
            create_bin_stats(special_values, max_bins, col_values)

    def test_creates_bin_ignores_nan_in_column(self):
        special_values = []
        max_bins = 10
        col_values = pd.Series([1, np.nan])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_has_mulitple_of_the_same_unique_value(self):
        special_values = []
        max_bins = 10
        col_values = pd.Series([1,1,1,1,1])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_ignores_infinite_value(self):
        special_values = []
        max_bins = 10
        col_values = pd.Series([1, np.inf])

        expected_output = [{
            'value': 1.0, 
            'percentage': 1.0, 
            'upper_edge': None
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)


        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_no_special_values(self):
        special_values = []
        max_bins = 10
        col_values = pd.Series([1, 2])

        expected_output = [{
            'percentage': 1.0,
            'upper_edge': 2
        }, {
            'percentage': 0.0,
            'upper_edge': np.inf
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_special_values_defined_but_none_in_column(self):
        special_values = [np.nan]
        max_bins = 10
        col_values = pd.Series([1, 2])

        expected_output = [{
            'value': np.nan,
            'percentage': 0.0
        }, {
            'percentage': 1.0,
            'upper_edge': 2
        }, {
            'percentage': 0.0,
            'upper_edge': np.inf
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        # print(output)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_special_values_defined_and_in_column(self):
        special_values = [np.nan]
        max_bins = 10
        col_values = pd.Series([1, 2, np.nan])

        expected_output = [{
            'value': np.nan,
            'percentage': 0.0
        }, {
            'percentage': 0.6666666666666666,
            'upper_edge': 2.0
        }, {
            'percentage': 0.0, 
            'upper_edge': np.inf
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        # print(output)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_special_values_defined_and_only_special_values_in_column(self):
        special_values = [-1]
        max_bins = 10
        col_values = pd.Series([-1, -1])

        expected_output = [{
            'value': -1, 
            'percentage': 1.0
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_creates_bin_for_column_with_special_values_defined_and_only_special_values_in_column(self):
        special_values = [-1]
        max_bins = 10
        col_values = pd.Series([-1, -1])

        expected_output = [{
            'value': -1, 
            'percentage': 1.0
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    def test_create_bin_for_columns_with_negative_max_bin(self):
        special_values = []
        max_bins = -1
        col_values = pd.Series([1, 21])

        with self.assertRaises(ValueError) as value_error:
            create_bin_stats(special_values, max_bins, col_values)


    def test_create_bin_for_columns_with_max_bin_as_float(self):
        special_values = []
        max_bins = 0.5
        col_values = pd.Series([1, 21])

        try:
            create_bin_stats(special_values, max_bins, col_values)
        except ValueError as value_error:
            self.assertTrue('must be defined as an integer' in str(value_error).lower())

    def test_create_bin_for_columns_with_unique_values_greater_than_max_bin(self):
        special_values = []
        max_bins = 2
        col_values = pd.Series([1,2,3,4])

        expected_output = [{
            'percentage': 0.75, 
            'upper_edge': 3
        }, {
            'percentage': 0.25, 
            'upper_edge': np.inf
        }]

        output = create_bin_stats(special_values, max_bins, col_values)
        self.assertEqual(expected_output, output)

    