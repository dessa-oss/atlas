"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import numpy as np
class DistributionChecker(object):   
    def __init__(self, distribution_options, bin_stats, reference_column_names):
        self._distribution_options = distribution_options.copy()
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

    def configure(self, attributes, threshold=None):
        if threshold != None:
            for column_name in attributes:
                self._distribution_options['custom_thresholds'][column_name] = threshold
        self._reference_column_names = set(self._reference_column_names).union(set(attributes))

    def exclude(self, attributes):
        if attributes == 'all':
            self._reference_column_names = set()
        else:
            self._reference_column_names = set(self._reference_column_names) - set(attributes)

    def validate(self, dataframe_to_validate):
        if dataframe_to_validate is None or len(dataframe_to_validate) == 0:
            raise ValueError('Invalid Dataframe provided')
        
        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        ##### PROTOTYPE CODE - rebuild distribution checker using TDD or Black-box based approach asap
        from foundations_orbit.contract_validators.prototype import distribution_and_special_values_check
        test_data = distribution_and_special_values_check(self._distribution_options, self._reference_column_names, self._bin_stats, dataframe_to_validate)
        
        return test_data