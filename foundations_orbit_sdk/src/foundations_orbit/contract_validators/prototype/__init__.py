"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
import pickle

from .utils import nand, count_and_remove_special_values, bin_current_values, add_special_value_l_infinity, \
    add_binned_metric


def bin_current_values_categorical(column_values, ref_column_bin_stats):
    current_category_percentages = {'other_bins':0}
    special_values_percentages = {}
    n_rows = len(column_values)
    current_unique_values = column_values.unique()

    category_bins, special_values_bin = [], []

    for category_bin in ref_column_bin_stats:
        if category_bin.get('category_value', None) != None:
            category_bins.append(category_bin['category_value'])
        elif category_bin.get('value', None) != None:
            special_values_bin.append(category_bin['value'])

    for unique_value in current_unique_values:
        if unique_value != unique_value:
            special_values_percentages[unique_value] = len(list(filter(lambda value: value != value, column_values)))/n_rows
        elif unique_value in category_bins:
            current_category_percentages[unique_value] = len(column_values[column_values == unique_value])/n_rows
        elif unique_value in special_values_bin:
            special_values_percentages[unique_value] = len(column_values[column_values == unique_value])/n_rows
        else:
            current_category_percentages['other_bins'] += len(column_values[column_values == unique_value])/n_rows

    return current_category_percentages, special_values_percentages


def distribution_and_special_values_check(distribution_check_config, column_names, bin_stats, current_df, categorical_attributes, is_special_value_check=False):
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
    dist_check_config = distribution_check_config
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

        ref_bin_percentages = []
        current_bin_percentages = []
        ref_special_values = []
        ref_special_value_percentages = []
        current_special_value_percentages = []

        if categorical_attributes[col]:
            dist_check_results[col] = {}
            column_values = current_df[col]
            ref_column_bin_stats = bin_stats[col]

            value_to_percentage_map = {}
            for unique_value_dict in ref_column_bin_stats:
                if unique_value_dict.get('category_value', None) != None:
                    value_to_percentage_map[str(unique_value_dict['category_value'])] = unique_value_dict['percentage']
                elif unique_value_dict.get('value', None) != None:
                    ref_special_values.append(unique_value_dict['value'])
                    value_to_percentage_map[str(unique_value_dict['value'])] = unique_value_dict['percentage']
                else:
                    value_to_percentage_map['other_bins'] = unique_value_dict['percentage']

            current_bin_percentages_dict, current_special_value_percentages_dict = bin_current_values_categorical(column_values, ref_column_bin_stats)

            for value_bin, current_value_percentage in current_bin_percentages_dict.items():
                ref_value_percentage = value_to_percentage_map[str(value_bin)]
                ref_bin_percentages.append(ref_value_percentage)
                current_bin_percentages.append(current_value_percentage)


            for value_bin, current_value_percentage in current_special_value_percentages_dict.items():
                ref_value_percentage = value_to_percentage_map[str(value_bin)]
                ref_special_value_percentages.append(ref_value_percentage)
                current_special_value_percentages.append(current_value_percentage)
        
        else:
            current_values = current_df[col].copy()
            n_current_vals = len(current_values)
            dist_check_results[col] = {}
            # bin the col in current_df using edges from reference
            ref_bin_percentages = []
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

        custom_method = dist_check_config['custom_methods'].get(col, None)
        method = custom_method if custom_method is not None else dist_check_config['distance_metric']
        add_binned_metric(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages, method)

    return dist_check_results
        
