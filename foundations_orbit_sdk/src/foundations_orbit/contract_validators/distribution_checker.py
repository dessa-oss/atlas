"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DistributionChecker(object):
    def __init__(self, reference_column_names, reference_column_types, categorical_attributes):

        self._initialize_default_options()

        self._categorical_attributes = categorical_attributes
        self._reference_column_names = reference_column_names
        self._reference_column_types = reference_column_types

        self._bin_stats = {}
        self._allowed_types = ['int', 'float', 'str', 'bool', 'datetime']

        self._initialize_exclusions()
        self._exclude_non_categorical_strings()

    def _initialize_exclusions(self):
        from foundations_orbit.contract_validators.checker import Checker

        self._column_names_to_exclude = set()
        self._invalid_attributes = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self.temp_attributes_to_exclude = []
        self._attributes_to_exclude_permanently = []

    def _initialize_default_options(self):
        self._distribution_options = {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'custom_thresholds': {},
            'custom_methods': {},
            'max_bins': 50
        }

    def _exclude_non_categorical_strings(self):
        for column in self._reference_column_names:
            non_categorical_string = not self._categorical_attributes[column] and 'str' in self._reference_column_types[column]
            if non_categorical_string:
                self._attributes_to_exclude_permanently.append(column)

    def __str__(self):
        return str(self.info())

    def info(self):
        return {
            'distribution_options': self._distribution_options,
            'bin_stats': self._bin_stats,
            'reference_column_names': self._reference_column_names,
            'reference_column_types': self._reference_column_types
        }

    def configure(self, attributes, threshold=None, method=None):
        self._check_configure_attributes(attributes)

        self._configure_thresholds(attributes, threshold)
        self._configure_methods(attributes, method)
        self._column_names_to_exclude = self._column_names_to_exclude.difference(set(attributes))

    def _check_configure_attributes(self, attributes):
        error_dictionary = {}

        for column in attributes:
            if column not in self._reference_column_names:
                error_dictionary[column] = 'Invalid Column Name: Does not exist in reference'
            elif column in self._invalid_attributes:
                error_dictionary[column] = f'Invalid Type: {self._reference_column_types[column]}'
        
        if error_dictionary != {}:
            raise ValueError(f'The following columns have errors: {error_dictionary}')

    def _configure_thresholds(self, attributes, threshold):
        if threshold is not None:
            for column_name in attributes:
                self._distribution_options['custom_thresholds'][column_name] = threshold

    def _configure_methods(self, attributes, method):
        if method is not None:
            for column_name in attributes:
                self._distribution_options['custom_methods'][column_name] = method

    def exclude(self, attributes):
        if attributes == 'all':
            self._column_names_to_exclude = set(self._reference_column_names)
        else:
            self._column_names_to_exclude = self._column_names_to_exclude.union(set(attributes))

    def temp_exclude(self, attributes):
        self.temp_attributes_to_exclude = attributes
        self.exclude(attributes=attributes)

    def validate(self, dataframe_to_validate):
        from foundations_orbit.contract_validators.prototype import distribution_check
        
        if dataframe_to_validate is None or len(dataframe_to_validate) == 0:
            raise ValueError('Invalid Dataframe provided')
        
        self.temp_exclude(self._attributes_to_exclude_permanently)

        column_names_to_validate = set(self._reference_column_names) - set(self._column_names_to_exclude)

        test_data = distribution_check(self._distribution_options, column_names_to_validate , self._bin_stats, dataframe_to_validate, categorical_attributes = self._categorical_attributes)
        
        self._reference_column_names = set(self._reference_column_names).union(set(self.temp_attributes_to_exclude))
        self.temp_attributes_to_exclude = []
        
        for attribute in self._attributes_to_exclude_permanently:
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