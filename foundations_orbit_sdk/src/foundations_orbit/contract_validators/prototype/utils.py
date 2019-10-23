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


def l_infinity(ref_percentages, current_percentages):
    return round(np.max(np.abs(np.array(ref_percentages) - np.array(current_percentages))), 3)

def entropy(pk, qk):
    return round(np.sum(pk * np.log(pk/qk), axis=0), 3)

def psi_score(ref_percentages, current_percentages):
    ref_percentages_array = np.array(ref_percentages)
    current_percentages_array = np.array(current_percentages)
    return entropy(ref_percentages_array, current_percentages_array) + entropy(current_percentages_array, ref_percentages_array)

def count_and_remove_special_values(ref_special_values, current_values):
    n_current_vals = len(current_values)
    # count and remove special values
    current_special_value_percentages = list()
    for sv in ref_special_values:
        if np.isnan(sv) and current_values.dtype.kind in {'u', 'i', 'f', 'c'}:
            sv_count = len(current_values[np.isnan(current_values)])
        elif not np.isnan(sv):
            sv_count = len(current_values[current_values == sv])
        else:
            sv_count = 0
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

        if np.isnan(sv):
            for key, value in threshold[col].items():
                if np.isnan(key):
                    value_to_check = value
        else:
            value_to_check = threshold[col][sv]

        if l_infinity_score < value_to_check:
            dist_check_results[col]['special_values'][sv]['passed'] = True
        else:
            dist_check_results[col]['special_values'][sv]['passed'] = False


def add_binned_metric(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages, method_name):
    if method_name == 'l_infinity':
        distance_metric = l_infinity(ref_bin_percentages, current_bin_percentages)
    elif method_name == 'psi':
        distance_metric = psi_score(ref_bin_percentages, current_bin_percentages)
    else:
        return

    dist_check_results[col][f'binned_{method_name}'] = distance_metric
    dist_check_results[col]['binned_passed'] = distance_metric < threshold