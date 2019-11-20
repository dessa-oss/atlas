"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
from foundations_orbit.contract_validators.prototype.utils import spread_counts_over_identical_edges


def create_bin_stats(max_bins, col_values):
    bin_dicts = []
    n_vals = col_values.size
    if n_vals < 1:
        raise ValueError('Invalid Column Values: Cannot create bin stats for empty column')

    if not isinstance(max_bins, int):
        raise ValueError('Invalid Max Bin: Max bin must be defined as an integer')

    if max_bins < 1:
        raise ValueError('Invalid Max Bin: Cannot create bin stats with bins less than 1.')

    if n_vals > 0:
        # make bins for all non-special values
        bin_counts, bin_edges = bin_values(col_values, max_bins)
        bin_percentages = list(np.array(bin_counts)/n_vals)
        # case: there is only one unique value
        if len(bin_edges) == 0:
            unique_value = col_values.iloc[0]
            bin_dicts.append({
                'value': unique_value,
                'percentage': len(col_values)/n_vals,
                'upper_edge': None
            })
        # otherwise there is more than one unique value
        else:
            for i, pct in enumerate(bin_percentages):
                bin_dict = {
                    "percentage": pct,
                    "upper_edge": bin_edges[i]
                }
                bin_dicts.append(bin_dict)

    return bin_dicts


def create_bin_stats_categorical(col_values, min_category_threshold=0.01):
    bin_dicts = []
    n_vals = col_values.size

    if n_vals == 0:
        return bin_dicts

    col_values.dropna(inplace=True)

    unique_value_percentages = col_values.value_counts(sort=False, normalize=True)
    valid_column_percentages = unique_value_percentages[unique_value_percentages >= min_category_threshold]
    other_percentage = 1.0 - valid_column_percentages.sum()
    for value in valid_column_percentages.index:
        bin_dicts.append({'category_value':value, 'percentage':round(valid_column_percentages.loc[value], 3)})

    bin_dicts.append({'other_bins':True, 'percentage':round(other_percentage, 3)})

    return bin_dicts

def bin_values(values, max_num_bins):
    values = values[values != np.inf]
    n_unique_values = values.nunique()
    if n_unique_values > 1:
        n_bins = get_num_bins(n_unique_values, max_num_bins)
        bin_counts, bin_edges = find_and_apply_edges(values, n_bins)
        bin_counts = spread_counts_over_identical_edges(bin_counts, bin_edges)
    else:
        bin_counts = [len(values), 0]
        bin_edges = []
    return bin_counts, bin_edges


def get_num_bins(unique_num, max_num_bins):
    '''based on the number of unique values provided, return the number of bins to apply'''
    # get number of unique values in the reference data
    if unique_num < max_num_bins:
        return unique_num
    else:
        return max_num_bins


def find_and_apply_edges(values, n_bins):
    from pandas import qcut

    bin_for_value, edges = qcut(values, n_bins, retbins=True, duplicates='drop')
    value_count_per_bin = bin_for_value.value_counts(sort=False).values
    truncated_edges = list(edges[1:-1])

    truncated_edges.append(np.inf)

    return value_count_per_bin, truncated_edges