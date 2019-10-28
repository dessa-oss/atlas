"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SpecialValuesChecker(object):

    def __init__(self, config_options, bin_stats, reference_column_names, reference_column_types, reference_dataframe=None):
        from foundations_orbit.contract_validators.checker import Checker

        self._config_options = config_options
        self._bin_stats = bin_stats
        self._reference_column_names = reference_column_names.copy() if reference_column_names else []
        self._config_columns = []
        self._config_options.distribution['special_value_thresholds'] = {}
        self._default_special_values = self._config_options.special_values
        self._column_special_values = self._initialize_columns_special_values()
        self._reference_dataframe = reference_dataframe

        self._allowed_types = ['int', 'float', 'str', 'bool', 'datetime']
        self._reference_column_types = reference_column_types
        self._invalid_attributes = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self.temp_attributes_to_exclude = []


    def _initialize_columns_special_values(self):
        _column_special_values = {}
        for column in self._reference_column_names:
            _column_special_values[column] = []
            for special_value in self._default_special_values:
                _column_special_values[column].append(special_value)
        return _column_special_values

    def validate(self, dataframe_to_validate):
        from foundations_orbit.contract_validators.prototype import distribution_and_special_values_check
        full_distribution_check_results = distribution_and_special_values_check(self._config_options.distribution, self._config_columns, self._bin_stats, dataframe_to_validate, True)
        special_values_results = {}
        for column, column_results in full_distribution_check_results.items():
            special_values_results[column] = {}
            for special_value, sv_details in column_results['special_values'].items():
                special_values_results[column][special_value] = sv_details
        
        self._config_columns = set(self._config_columns).union(set(self.temp_attributes_to_exclude))
        self.temp_attributes_to_exclude = []

        return special_values_results

    def configure(self, attributes=None, thresholds=None):
        if attributes is None:
            raise ValueError('Invalid attribute: The attribute is required for configuration')
        if thresholds is None:
            raise ValueError('Invalid threshold: The threshold is required for configuration')
        if not isinstance(thresholds, dict):
            raise ValueError('Invalid threshold: thresholds must be specified using dictionaries')

        to_be_recalculate = False
        columns_to_be_recalculation = {}
        
        error_dictionary = {}
        for column in attributes:
            if column in self._invalid_attributes:
                error_dictionary[column] = self._reference_column_types[column]

        if error_dictionary != {}:
            raise ValueError(f'The following columns have invalid types: {error_dictionary}')

        for column in attributes:
            to_be_recalculate = self._check_if_column_needs_bin_recalculation(columns_to_be_recalculation, column, thresholds) or to_be_recalculate
            column_threshold = {
                column: thresholds
            }

            self._config_options.distribution['special_value_thresholds'].update(column_threshold)

        self._config_columns = list(set(self._config_columns).union(set(attributes)))

        if to_be_recalculate:
            self._recalculate_column_bin_stats(columns_to_be_recalculation)

    def _check_if_column_needs_bin_recalculation(self, columns_need_bin_recalculation, column, thresholds):
        needs_bin_recalculation = False
        columns_need_bin_recalculation[column] = False
        for special_value, threshold in thresholds.items():
            if special_value not in self._column_special_values[column]:
                needs_bin_recalculation = True
                columns_need_bin_recalculation[column] = True
                self._column_special_values[column].append(special_value)
        return needs_bin_recalculation

    def _recalculate_column_bin_stats(self, columns_need_bin_recalculation):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
        for column in columns_need_bin_recalculation:
            if columns_need_bin_recalculation[column]:
                self._bin_stats[column] = create_bin_stats(self._column_special_values[column], self._config_options.max_bins, self._reference_dataframe[column])

    def exclude(self, attributes):
        if attributes == 'all':
            self._config_columns = []
        else:
            self._config_columns = set(self._config_columns) - set(attributes)

    def temp_exclude(self, attributes):
        self.temp_attributes_to_exclude = attributes
        self.exclude(attributes=attributes)