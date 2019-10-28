"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
from foundations_orbit.contract_validators.prototype.utils import spread_counts_over_identical_edges


def create_bin_stats(special_values, max_bins, col_values):
    bin_dicts = []
    n_vals = len(col_values)
    if n_vals < 1:
        raise ValueError('Invalid Column Values: Cannot create bin stats for empty column')

    if not isinstance(max_bins, int):
        raise ValueError('Invalid Max Bin: Max bin must be defined as an integer')

    if max_bins < 1:
        raise ValueError('Invalid Max Bin: Cannot create bin stats with bins less than 1.')
    # for every special value, make a bin for it
    for sv in special_values:
        if sv is np.nan:
            sv_count = col_values.isna().sum()
        else:
            sv_count = len(col_values[col_values == sv])

        sv_dict = {'value': sv, "percentage": sv_count/n_vals}
        # drop current special value
        col_values = col_values[col_values != sv]
        bin_dicts.append(sv_dict)

    if len(col_values) > 0:
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
            bin_edges.append(np.inf)
            for i, pct in enumerate(bin_percentages):
                bin_dict = {
                    "percentage": pct,
                    "upper_edge": bin_edges[i]
                }
                bin_dicts.append(bin_dict)

    return bin_dicts


def bin_values(values, max_num_bins):
    values = values[values != np.inf]
    n_unique_values = values.nunique()
    if n_unique_values > 1:
        n_bins = get_num_bins(values, max_num_bins)
        bin_counts, bin_edges = find_and_apply_edges(values, n_bins)
        bin_counts = spread_counts_over_identical_edges(bin_counts, bin_edges)
    else:
        bin_counts = [len(values), 0]
        bin_edges = []
    return bin_counts, bin_edges


def get_num_bins(values, max_num_bins):
    '''based on the number of unique values provided, return the number of bins to apply'''
    # get number of unique values in the reference data
    unique_num = values.nunique()
    if unique_num < max_num_bins:
        return unique_num
    else:
        return max_num_bins


def find_and_apply_edges(values, n_bins):
    '''find edges and find count in each bin'''
    values_sorted = values.sort_values().dropna()
    values_length = values_sorted.shape[0]
    # edges are values from values_sorted taken such that each bin contains the same number of elements
    edges = [values_sorted.iloc[int(np.floor(values_length * i / n_bins))] for i in range(1, n_bins)]
    binned_values = [0] + [values_sorted[values_sorted <= i].shape[0] for i in edges]
    binned_values = np.diff(binned_values, axis=0)
    binned_values = np.append(binned_values, values_sorted[values_sorted > edges[-1]].shape[0])
    return binned_values, edges

