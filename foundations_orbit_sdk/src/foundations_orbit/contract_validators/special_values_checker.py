"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
class SpecialValuesChecker(object):

    def __init__(self, config_options, bin_stats, reference_column_names):
        self._config_options = config_options.copy()
        self._bin_stats = bin_stats
        self._reference_column_names = reference_column_names.copy() if reference_column_names else []
        self._config_columns = []
        self._config_options['special_value_thresholds'] = {}

    def validate(self, dataframe_to_validate):
        from foundations_orbit.contract_validators.prototype import distribution_and_special_values_check
        full_distribution_check_results = distribution_and_special_values_check(self._config_options, self._config_columns, self._bin_stats, dataframe_to_validate, True)
        
        special_values_results = {}
        for column, column_results in full_distribution_check_results.items():
            special_values_results[column] = {}
            for special_value, sv_details in column_results['special_values'].items():
                special_values_results[column][special_value] = sv_details
        
        return special_values_results

    def configure(self, attributes=None, thresholds=None):
        if attributes == None:
            raise ValueError('Invalid attribute: The attribute is required for configuration')
        if thresholds == None:
            raise ValueError('Invalid threshold: The threshold is required for configuration')
        if not isinstance(thresholds, dict):
            raise ValueError('Invalid threshold: thresholds must be specified using dictionaries')

        for column in attributes:
            column_threshold = {
                column: thresholds
            }
            self._config_options['special_value_thresholds'].update(column_threshold)

        self._config_columns = list(set(self._config_columns).union(set(attributes)))

    def exclude(self, attributes):
        if attributes == 'all':
            self._config_columns = []
        else:
            self._config_columns = set(self._config_columns) - set(attributes)