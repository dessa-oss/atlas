"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
import pickle

from .utils import nand, count_and_remove_special_values, bin_current_values, add_special_value_l_infinity, \
    add_binned_l_infinity


def distribution_and_special_values_check(config_dict, column_names, bin_stats, current_df, is_special_value_check=False):
    '''
        Expected format of dist_check_results
        {'col1': {'binned_passed': False,
                'binned_l_infinity': 0.2,
                'special_values':
                    {'nan':
                        {'percentage_diff': 0.15, 'ref_percentage': 0, 'current_percentage': 0.15, 'passed': True}
                    }
                }
    :param ref_col_stats:
    :param current_df:
    :return:
    '''
    dist_check_results = {}
    # get the list of columns to check
    dist_check_config = config_dict
    cols_to_check = set(current_df.columns).intersection(set(column_names))
    # only one of cols_to_check and cols_to_ignore can be non-None
    assert nand(dist_check_config['cols_to_include'] is not None, dist_check_config['cols_to_ignore'] is not None)
    
    if dist_check_config['cols_to_include'] is not None:
        cols_to_check = set(dist_check_config['cols_to_include']).intersection(cols_to_check)
    elif dist_check_config['cols_to_ignore'] is not None:
        cols_to_check = cols_to_check - set(dist_check_config['cols_to_ignore'])

    # apply check to each col in cols_to_check
    cols_to_check = [col for col in current_df.columns if col in cols_to_check] # use same order as current_df

    # for each column extract relevant information (bin stats + special values)
    for col in cols_to_check:
        current_values = current_df[col].copy()
        n_current_vals = len(current_values)
        dist_check_results[col] = {}
        # bin the col in current_df using edges from reference
        ref_special_value_percentages = []
        ref_bin_percentages = []
        ref_special_values = []
        ref_edges = []
        unique_ref_value = None
        ref_bin_stats = bin_stats[col]
        for bin in ref_bin_stats:
            # special value
            if 'upper_edge' not in bin:
                ref_special_values.append(bin['value'])
                ref_special_value_percentages.append(bin['percentage'])
            # unique value
            elif 'upper_edge' in bin and bin['upper_edge'] is None:
                unique_ref_value = bin['value']
                ref_bin_percentages.append(bin['percentage'])
                ref_bin_percentages.append(0)  # to compare with current_other_value_counts percentage
            # normal bins
            else:
                ref_bin_percentages.append(bin['percentage'])
                # the upper_edge of the bin with the largest values is np.inf, ref_edges shouldn't include this
                if bin['upper_edge'] != np.inf:
                    ref_edges.append(bin['upper_edge'])

        # accounting for special values
        current_values, current_special_value_percentages = count_and_remove_special_values(ref_special_values, current_values)

        # binning current_values
        current_bin_percentages = bin_current_values(current_values, ref_edges, n_current_vals, unique_ref_value)

        # define threshold for l_infinity tests
        custom_threshold = dist_check_config['custom_thresholds'].get(col, None)
        threshold = custom_threshold if custom_threshold != None else dist_check_config['default_threshold']
        if is_special_value_check:
            sv_threshold = dist_check_config['special_value_thresholds']
            # add l_infinity test results to dist_check_results (special_values)
            add_special_value_l_infinity(col, sv_threshold, dist_check_results, ref_special_values,
                                            ref_special_value_percentages, current_special_value_percentages)

        # add l_infinity test results to dist_check_results (distribution)
        add_binned_l_infinity(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages)

    return dist_check_results