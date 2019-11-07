"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SpecialValuesChecker(object):

    def __init__(self, reference_column_names, reference_column_types, categorical_attributes):
        from foundations_orbit.contract_validators.checker import Checker
        import numpy
        self._special_value_thresholds = {}
        self._special_value_percentages = None
        self._reference_column_names = reference_column_names.copy() if reference_column_names else []
        self._config_columns = []
        self._allowed_types = ['int', 'float', 'str', 'bool', 'datetime']
        self._reference_column_types = reference_column_types
        self._invalid_attributes = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self.temp_attributes_to_exclude = []

        self._categorical_attributes = categorical_attributes

    def __str__(self):
        return str(self._special_value_thresholds)

    def validate(self, dataframe_to_validate):
        self._config_columns = set(self._config_columns).union(set(self.temp_attributes_to_exclude))
        self.temp_attributes_to_exclude = []

        special_values_results = self._special_values_check(dataframe_to_validate)

        return special_values_results

    def _special_values_check(self, dataframe_to_validate):
        dataframe_to_validate_special_value_percentages = self._create_special_value_percentages_for_dataframe(dataframe_to_validate)
        results = {}

        columns_to_check = set(self._special_value_thresholds.keys()).intersection(set(self._config_columns))

        for column in columns_to_check:
            results[column] = self._special_values_check_for_column(dataframe_to_validate_special_value_percentages, column)

        return results

    def _special_values_check_for_column(self, dataframe_to_validate_special_value_percentages, column):
        column_results = {}

        for special_value, reference_threshold in self._special_value_thresholds[column].items():
            column_results[special_value] = self._special_values_check_for_special_value_in_column(dataframe_to_validate_special_value_percentages, column, special_value, reference_threshold)

        return column_results

    def _special_values_check_for_special_value_in_column(self, dataframe_to_validate_special_value_percentages, column, special_value, reference_threshold):
        import numpy

        special_value_results = {}

        if numpy.isnan(special_value):
            for key, value in self._special_value_percentages[column].items():
                if numpy.isnan(key):
                    reference_percentage = value
        else:
            reference_percentage = self._special_value_percentages[column][special_value]

        current_percentage = dataframe_to_validate_special_value_percentages[column][special_value]
        absolute_difference = abs(current_percentage - reference_percentage)

        if absolute_difference > reference_threshold:
            special_value_results['passed'] = False
        else:
            special_value_results['passed'] = True

        special_value_results['percentage_diff'] = absolute_difference
        special_value_results['ref_percentage'] = reference_percentage
        special_value_results['current_percentage'] = current_percentage

        return special_value_results

    def _create_special_value_percentages_for_dataframe(self, dataframe):
        import math

        special_value_percentages = {}
        num_rows_in_df = len(dataframe)

        for column, threshold_dictionary in self._special_value_thresholds.items():
            special_value_percentages[column] = {}
            series_to_validate = dataframe[column]
            for special_value, _ in threshold_dictionary.items():
                if math.isnan(special_value):
                    num_special_values = series_to_validate.isna().sum()
                else:
                    num_special_values = len(series_to_validate[series_to_validate == special_value])
                special_value_percentage = num_special_values/num_rows_in_df
                special_value_percentages[column][special_value] = special_value_percentage

        return special_value_percentages

    def configure(self, attributes=None, thresholds=None, mode='overwrite'):
        if attributes is None:
            raise ValueError('Invalid attribute: The attribute is required for configuration')
        if thresholds is None:
            raise ValueError('Invalid threshold: The threshold is required for configuration')
        if not isinstance(thresholds, dict):
            raise ValueError('Invalid threshold: thresholds must be specified using dictionaries')

        error_dictionary = {}
        for column in attributes:
            if column in self._invalid_attributes:
                error_dictionary[column] = self._reference_column_types[column]

        if error_dictionary != {}:
            raise ValueError(f'The following columns have invalid types: {error_dictionary}')

        for column in attributes:

            # if mode == 'overwrite':
            #     self._special_value_thresholds[column] = thresholds
            # elif mode == 'update':
            for special_value, threshold in thresholds.items():
                if not self._special_value_thresholds.get(column, False):
                    self._special_value_thresholds[column] = {}
                self._special_value_thresholds[column][special_value] = threshold

        self._config_columns = list(set(self._config_columns).union(set(attributes)))

    def exclude(self, attributes):
        if attributes == 'all':
            self._config_columns = []
        else:
            self._config_columns = set(self._config_columns) - set(attributes)

    def temp_exclude(self, attributes):
        self.temp_attributes_to_exclude = attributes
        self.exclude(attributes=attributes)

    def create_and_set_special_value_percentages(self, reference_dataframe):
        self._special_value_percentages = self._create_special_value_percentages_for_dataframe(reference_dataframe)