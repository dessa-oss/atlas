"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


# NB - KD - Insufficiently tested... Feel free to disregard and follow proper TDD
import numpy as np
class DistributionChecker(object):
    '''
    Expected format of dist_check_results
        {
            'col1': {
                'binned_passed': False,
                'binned_l_infinity': 0.2,
                'special_values':{
                    'nan':{
                        'percentage_diff': 0.15, 'ref_percentage': 0, 
                        'current_percentage': 0.15, 'passed': True
                    }
                }
            }
        }
    '''
    
    def __init__(self, distribution_options, column_names, bin_stats, current_df):
        self._distribution_options = distribution_options
        self._column_names = column_names
        self._bin_stats = bin_stats
        self._current_df = current_df

    def distribution_check_results(self):
        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        dist_check_results = {}

        results_for_same_distribution = {
            'binned_l_infinity': 0.0,
            'binned_passed': True,
            'special_values': {
                np.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        columns_to_check = self._column_names.copy()

        for column_name in columns_to_check:
            dist_check_results[column_name] = results_for_same_distribution
            column_check_resuls = dist_check_results[column_name]
            current_values = self._current_df[column_name].copy()
            n_current_vals = len(current_values)
            ref_special_value_percentages = []
            ref_bin_percentages = []
            ref_special_values = []
            ref_edges = []
            unique_ref_value = None
            ref_bin_stats = self._bin_stats[column_name]

            for bin in ref_bin_stats:
                if 'upper_edge' not in bin: # special value
                    ref_special_values.append(bin['value'])
                    ref_special_value_percentages.append(bin['percentage'])
                elif 'upper_edge' in bin and bin['upper_edge'] is None: # unique value
                    unique_ref_value = bin['value']
                    ref_bin_percentages.append(bin['percentage'])
                    ref_bin_percentages.append(0)  # to compare with current_other_value_counts percentage
                else: # normal nin
                    ref_bin_percentages.append(bin['percentage'])
                    # the upper_edge of the bin with the largest values is np.inf, ref_edges shouldn't include this
                    if bin['upper_edge'] != np.inf:
                        ref_edges.append(bin['upper_edge'])

            current_special_value_percentages = self._count_special_values(ref_special_values, current_values)
            current_values = self._remove_special_values(ref_special_values, current_values)
            current_bin_percentages = self._bin_current_values(current_values, ref_edges, n_current_vals, unique_ref_value)

            # define threshold for l_infinity tests
            custom_threshold = self._distribution_options['custom_thresholds'].get(column_name, None)
            threshold = custom_threshold if custom_threshold != None else self._distribution_options['default_threshold']

            column_check_resuls['special_values'] = self._special_value_l_infinity(threshold,
                                                                            ref_special_values, 
                                                                            ref_special_value_percentages, 
                                                                            current_special_value_percentages)

            column_check_resuls['binned_l_infinity'] = self._l_infinity(ref_bin_percentages, current_bin_percentages)
            column_check_resuls['binned_passed'] = column_check_resuls['binned_l_infinity'] < threshold

        return dist_check_results

    def _count_special_values(self, ref_special_values, current_values):
        n_current_vals = len(current_values)
        # count and remove special values
        current_special_value_percentages = list()
        for sv in ref_special_values:
            if np.isnan(sv):
                sv_count = len(current_values[np.isnan(current_values)])
            else:
                sv_count = len(current_values[current_values == sv])
            current_special_value_percentages.append(sv_count / n_current_vals)
        return current_special_value_percentages

    def _remove_special_values(self, ref_special_values, current_values):
        values = current_values.copy()
        for sv in ref_special_values:
            values = values[values != sv]
        return values

    def _bin_current_values(self, current_values, ref_edges, n_current_vals, unique_ref_value):
        if len(ref_edges) > 0: # typical case where there was more than 1 unique-valued bin in the reference
            current_bin_value_counts = self._apply_edges(current_values, ref_edges)
            current_bin_value_counts = self._spread_counts_over_identical_edges(current_bin_value_counts, ref_edges)
            current_bin_percentages = np.array(current_bin_value_counts) / n_current_vals
        else: # case where there is only one bin in the reference
            current_unique_ref_value_count = len(current_values[current_values == unique_ref_value])
            current_other_value_count = len(current_values[current_values != unique_ref_value])
            current_bin_percentages = np.array([current_unique_ref_value_count, current_other_value_count]) / n_current_vals
        return current_bin_percentages

    def _special_value_l_infinity(self, threshold, ref_special_values, ref_special_value_percentages, current_special_value_percentages):
        special_values = {}
        for sv, ref_pct, cur_pct in zip(ref_special_values, ref_special_value_percentages, current_special_value_percentages):
            special_values[sv] = {}
            l_infinity_score = self._l_infinity(ref_pct, cur_pct)
            special_values[sv]['percentage_diff'] = l_infinity_score
            special_values[sv]['ref_percentage'] = ref_pct
            special_values[sv]['current_percentage'] = cur_pct

            if l_infinity_score < threshold:
                special_values[sv]['passed'] = True
            else:
                special_values[sv]['passed'] = False

        return special_values

    def _l_infinity(self, ref_percentages, current_percentages):
        return np.max(np.abs(np.array(ref_percentages) - np.array(current_percentages)))

    # NB - apply edges changes (2, ) vector to (3, ) causes test with upper edge and non special values to break
    def _apply_edges(self, values, edges):
        '''find corresponding bin counts using provided bin edges'''
        binned_values = [0] + [values[values <= i].shape[0] for i in edges]
        binned_values = np.diff(binned_values, axis=0)
        binned_values = np.append(binned_values, values[values > edges[-1]].shape[0])
        return binned_values
    
    def _spread_counts_over_identical_edges(self, binned_values, edges):
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