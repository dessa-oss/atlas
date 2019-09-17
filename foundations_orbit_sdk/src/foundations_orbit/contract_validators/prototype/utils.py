"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
from copy import deepcopy


def nand(a,b):
    return not (a and b)

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


def apply_edges(values, edges):
    '''find corresponding bin counts using provided bin edges'''
    binned_values = [0] + [values[values <= i].shape[0] for i in edges]
    binned_values = np.diff(binned_values, axis=0)
    binned_values = np.append(binned_values, values[values > edges[-1]].shape[0])
    return binned_values


def spread_counts_over_identical_edges(binned_values, edges):
    '''check for edges that are consecutive; spread out counts over bins with identical edges'''
    i = 0
    while i < len(edges) - 1:
        j = i + 1
        while j < len(edges) and edges[j] == edges[i]:
            j += 1
        if j - i > 1:
            s = binned_values[i:j].sum()
            binned_values[i:j] = s // (j - i)
            binned_values[i] = binned_values[i] + (s % (j - i))
        i = j
    return binned_values


def bin_values(values, max_num_bins):
    n_unique_values = values.nunique()
    if n_unique_values > 1:
        n_bins = get_num_bins(values, max_num_bins)
        bin_counts, bin_edges = find_and_apply_edges(values, n_bins)
        bin_counts = spread_counts_over_identical_edges(bin_counts, bin_edges)
    else:
        bin_counts = [len(values), 0]
        bin_edges = []
    return bin_counts, bin_edges

def l_infinity(ref_percentages, current_percentages):
    return np.max(np.abs(np.array(ref_percentages) - np.array(current_percentages)))

def l_infinity_test(ref_percentages, current_percentages, threshold):
    l_infinity_score = l_infinity(ref_percentages, current_percentages)
    return l_infinity_score < threshold


def count_and_remove_special_values(ref_special_values, current_values):
    n_current_vals = len(current_values)
    # count and remove special values
    current_special_value_percentages = list()
    print(ref_special_values)
    for sv in ref_special_values:
        print(f'THE SV IS {sv}')
        if np.isnan(sv):
            sv_count = len(current_values[np.isnan(current_values)])
        else:
            sv_count = len(current_values[current_values == sv])
        current_special_value_percentages.append(sv_count / n_current_vals)
        # drop current special value
        current_values = current_values[current_values != sv]
    return current_values, current_special_value_percentages

def bin_current_values(current_values, ref_edges, n_current_vals, unique_ref_value):
    # typical case where there was more than 1 unique-valued bin in the reference
    if len(ref_edges) > 0:
        current_bin_value_counts = apply_edges(current_values, ref_edges)
        current_bin_value_counts = spread_counts_over_identical_edges(current_bin_value_counts, ref_edges)
        current_bin_percentages = np.array(current_bin_value_counts) / n_current_vals
    # case where there is only one bin in the reference
    else:
        current_unique_ref_value_count = len(current_values[current_values == unique_ref_value])
        current_other_value_count = len(current_values[current_values != unique_ref_value])
        current_bin_percentages = np.array([current_unique_ref_value_count, current_other_value_count]) / n_current_vals
    return current_bin_percentages


def add_special_value_l_infinity(col, threshold, dist_check_results, ref_special_values, ref_special_value_percentages,
                       current_special_value_percentages):
    # percentage differences for special values
    dist_check_results[col]['special_values'] = {}
    for sv, ref_pct, cur_pct in zip(ref_special_values, ref_special_value_percentages,
                                    current_special_value_percentages):
        dist_check_results[col]['special_values'][sv] = {}
        l_infinity_score = l_infinity(ref_pct, cur_pct)
        dist_check_results[col]['special_values'][sv]['percentage_diff'] = l_infinity_score
        dist_check_results[col]['special_values'][sv]['ref_percentage'] = ref_pct
        dist_check_results[col]['special_values'][sv]['current_percentage'] = cur_pct

        if l_infinity_score < threshold:
            dist_check_results[col]['special_values'][sv]['passed'] = True
        else:
            dist_check_results[col]['special_values'][sv]['passed'] = False


def add_binned_l_infinity(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages):
    # l-infinity test for the rest of the bins
    l_infinity_score = l_infinity(ref_bin_percentages, current_bin_percentages)
    dist_check_results[col]['binned_l_infinity'] = l_infinity_score
    if l_infinity_score < threshold:
        dist_check_results[col]['binned_passed'] = True
    else:
        dist_check_results[col]['binned_passed'] = False