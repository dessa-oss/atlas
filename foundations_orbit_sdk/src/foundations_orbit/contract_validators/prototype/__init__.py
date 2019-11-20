"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
import pickle

from .utils import nand, bin_current_values, add_special_value_l_infinity, \
    add_binned_metric


def bin_current_values_categorical(column_values, ref_column_bin_stats):
    current_category_percentages = {'other_bins':0}
    n_rows = column_values.size

    column_value_counts = column_values.value_counts(sort=False, normalize=True)
    current_unique_values = column_value_counts.index

    category_bins = []

    for category_bin in ref_column_bin_stats:
        if category_bin.get('category_value', None) != None:
            category_bins.append(category_bin['category_value'])

    current_unique_values_not_in_ref = column_value_counts[~column_value_counts.index.isin(category_bins)].index
    current_category_percentages['other_bins'] = column_value_counts[current_unique_values_not_in_ref].sum()
    remaining_values_in_current_unique_values = set(current_unique_values) - set(current_unique_values_not_in_ref)

    dict_of_remaining_current_category_pct =  column_value_counts[remaining_values_in_current_unique_values].to_dict()
    current_category_percentages = {**dict_of_remaining_current_category_pct, **current_category_percentages}

    return current_category_percentages


def distribution_check(distribution_check_config, column_names, bin_stats, current_df, categorical_attributes, is_special_value_check=False):
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
    # apply check to each col in cols_to_check
    cols_to_check = [col for col in current_df.columns if col in cols_to_check] # use same order as current_df

    # for each column extract relevant information (bin stats + special values)
    for col in cols_to_check:

        ref_bin_percentages = []
        current_bin_percentages = []

        if categorical_attributes[col]:
            dist_check_results[col] = {}
            column_values = current_df[col]
            ref_column_bin_stats = bin_stats[col]

            value_to_percentage_map = {}
            for unique_value_dict in ref_column_bin_stats:
                if unique_value_dict.get('category_value', None) != None:
                    value_to_percentage_map[str(unique_value_dict['category_value'])] = unique_value_dict['percentage']
                else:
                    value_to_percentage_map['other_bins'] = unique_value_dict['percentage']

            current_bin_percentages_dict = bin_current_values_categorical(column_values, ref_column_bin_stats)

            for value_bin, current_value_percentage in current_bin_percentages_dict.items():
                ref_value_percentage = value_to_percentage_map[str(value_bin)]
                ref_bin_percentages.append(ref_value_percentage)
                current_bin_percentages.append(current_value_percentage)
        else:
            current_values = current_df[col].copy()
            n_current_vals = len(current_values)
            dist_check_results[col] = {}
            # bin the col in current_df using edges from reference
            ref_bin_percentages = []
            ref_edges = []
            unique_ref_value = None
            ref_bin_stats = bin_stats[col]

            if ref_bin_stats:
                # print(ref_bin_stats)
                for bin in ref_bin_stats:
                    # special value
                    if 'upper_edge' in bin and bin['upper_edge'] is None:
                        unique_ref_value = bin['value']
                        ref_bin_percentages.append(bin['percentage'])
                        ref_bin_percentages.append(0)  # to compare with current_other_value_counts percentage
                    # normal bins
                    else:
                        ref_bin_percentages.append(bin['percentage'])

                        # the upper_edge of the bin with the largest values is np.inf, ref_edges shouldn't include this
                        ref_edges.append(bin['upper_edge'])
                # binning current_values
                current_bin_percentages = bin_current_values(current_values, ref_edges, n_current_vals, unique_ref_value)
            else:  # There is no reference bin stats
                current_bin_percentages = None

        # define threshold for l_infinity tests
        custom_threshold = dist_check_config['custom_thresholds'].get(col, None)
        threshold = custom_threshold if custom_threshold != None else dist_check_config['default_threshold']

        custom_method = dist_check_config['custom_methods'].get(col, None)
        method = custom_method if custom_method is not None else dist_check_config['distance_metric']
        add_binned_metric(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages, method)

    return dist_check_results

