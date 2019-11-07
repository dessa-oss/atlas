"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import numpy as np
class DistributionChecker(object):   
    def __init__(self, distribution_options, reference_column_names, reference_column_types, categorical_attributes):
        from foundations_orbit.contract_validators.checker import Checker
        self._categorical_attributes = categorical_attributes
        self._distribution_options = distribution_options.copy()
        self._distribution_options.update({'max_bins': 50})
        self._bin_stats = {}
        self._reference_column_names = reference_column_names
        self._reference_column_types = reference_column_types
        self._allowed_types = ['int', 'float', 'str', 'bool', 'datetime']
        self._invalid_attributes = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self.temp_attributes_to_exclude = []
        self._attributes_to_exclude = []
        for column in reference_column_names:
            if not categorical_attributes[column] and 'str' in reference_column_types[column]:
                self._attributes_to_exclude.append(column)

    def __str__(self):
        import json

        information =  {
            'distribution_options': self._distribution_options,
            'bin_stats': self._bin_stats,
            'reference_column_names': self._reference_column_names,
            'reference_column_types': self._reference_column_types
        }

        # return json.dumps(information)
        return str(information)

    def configure(self, attributes, threshold=None, method=None):
        error_dictionary = {}
        for column in attributes:
            if column in self._invalid_attributes:
                error_dictionary[column] = self._reference_column_types[column]

        if error_dictionary != {}:
            raise ValueError(f'The following columns have invalid types: {error_dictionary}')

        if threshold is not None:
            for column_name in attributes:
                self._distribution_options['custom_thresholds'][column_name] = threshold
        if method is not None:
            for column_name in attributes:
                self._distribution_options['custom_methods'][column_name] = method

        self._reference_column_names = set(self._reference_column_names).union(set(attributes))

    def exclude(self, attributes):
        if attributes == 'all':
            self._reference_column_names = set()
        else:
            self._reference_column_names = set(self._reference_column_names) - set(attributes)

    def temp_exclude(self, attributes):
        self.temp_attributes_to_exclude = attributes
        self.exclude(attributes=attributes)

    def validate(self, dataframe_to_validate):
        if dataframe_to_validate is None or len(dataframe_to_validate) == 0:
            raise ValueError('Invalid Dataframe provided')
        
        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')
        
        self.temp_exclude(self._attributes_to_exclude)
        ##### PROTOTYPE CODE - rebuild distribution checker using TDD or Black-box based approach asap
        from foundations_orbit.contract_validators.prototype import distribution_check
        test_data = distribution_check(self._distribution_options, self._reference_column_names, self._bin_stats, dataframe_to_validate, categorical_attributes = self._categorical_attributes)
        
        self._reference_column_names = set(self._reference_column_names).union(set(self.temp_attributes_to_exclude))
        self.temp_attributes_to_exclude = []
        
        for attribute in self._attributes_to_exclude:
            test_data[attribute] = {"binned_passed": False, 'message': "non-categorical strings are not supported"}
        return test_data

    def create_and_set_bin_stats(self, reference_dataframe):
        self._calculate_bin_stats(reference_dataframe)

    def _calculate_bin_stats(self, reference_dataframe):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical

        for column_name in self._reference_column_names:
            if self._categorical_attributes[column_name]:
                self._bin_stats[column_name] = create_bin_stats_categorical(reference_dataframe[column_name])
            else:
                self._bin_stats[column_name] = create_bin_stats(self._distribution_options['max_bins'], reference_dataframe[column_name])