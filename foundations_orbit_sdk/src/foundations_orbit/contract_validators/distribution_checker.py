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
    
    def __init__(self, distribution_options, bin_stats, reference_column_names):
        self._distribution_options = distribution_options
        self._bin_stats = bin_stats
        self._reference_column_names = reference_column_names

    def validate(self, dataframe_to_validate):
        if dataframe_to_validate is None or len(dataframe_to_validate) == 0:
            raise ValueError('Invalid Dataframe provided')
        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        from foundations_orbit.contract_validators.prototype import distribution_check

        return distribution_check(self._distribution_options, self._reference_column_names, self._bin_stats, dataframe_to_validate)

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
        return round(np.max(np.abs(np.array(ref_percentages) - np.array(current_percentages))), 3)

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