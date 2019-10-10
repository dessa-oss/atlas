"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
class SpecialValuesChecker(object):

    def __init__(self, config_options, bin_stats, reference_column_names):
        self._config_options = config_options
        self._bin_stats = bin_stats
        self._reference_column_names = reference_column_names

    def validate(self, dataframe_to_validate):
        from foundations_orbit.contract_validators.prototype import distribution_and_special_values_check
        full_distribution_check_results = distribution_and_special_values_check(self._config_options, self._reference_column_names, self._bin_stats, dataframe_to_validate)
        
        special_values_results = {}
        for column, column_results in full_distribution_check_results.items():
            special_values_results[column] = {}
            for special_value, sv_details in column_results['special_values'].items():
                special_values_results[column][special_value] = sv_details
        
        return special_values_results

    def configure(self, attributes):
        self._reference_column_names = attributes

    def exclude(self, attributes):
        self._reference_column_names = set(self._reference_column_names) - set(attributes)