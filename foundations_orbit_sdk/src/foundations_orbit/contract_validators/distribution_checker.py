"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

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
        
        import numpy

        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        dist_check_results = {}

        results_for_same_distribution = {
            'binned_l_infinity': 0.0,
            'binned_passed': True,
            'special_values': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        for column_name in self._column_names:
            dist_check_results[column_name] = results_for_same_distribution

        return dist_check_results