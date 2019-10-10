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

    def __str__(self):
        import json

        information =  {
            'distribution_options': self._distribution_options,
            'bin_stats': self._bin_stats,
            'reference_column_names': self._reference_column_names
        }

        return json.dumps(information)

    def configure(self, attributes):
        self._reference_column_names = attributes

    def exclude(self, attributes):
        self._reference_column_names = set(self._reference_column_names) - set(attributes)

    def validate(self, dataframe_to_validate):
        if dataframe_to_validate is None or len(dataframe_to_validate) == 0:
            raise ValueError('Invalid Dataframe provided')
        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        from foundations_orbit.contract_validators.prototype import distribution_check

        return distribution_check(self._distribution_options, self._reference_column_names, self._bin_stats, dataframe_to_validate)