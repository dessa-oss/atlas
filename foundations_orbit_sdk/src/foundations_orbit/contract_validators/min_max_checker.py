"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_orbit.contract_validators.checker import Checker
class MinMaxChecker(object):

    def __init__(self, reference_column_types):
        self.columns_to_bounds = {}
        self._reference_column_types = reference_column_types
        self._allowed_types = ['int', 'float', 'datetime']
        self._columns_excluded_for_type_mismatch = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self._columns_to_bounds_temp = {}

    def configure(self, columns, lower_bound=None, upper_bound=None):
        error_dictionary = {}
        if lower_bound is None and upper_bound is None:
            raise ValueError('expected either lower and/or upper bound')

        for attribute in columns:
            if attribute in self._columns_excluded_for_type_mismatch:
                error_dictionary[attribute] = self._reference_column_types[attribute]
            else:
                self.columns_to_bounds[attribute] = {
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }

        if error_dictionary != {}:
            self.columns_to_bounds = {}
            raise ValueError(f'The following columns have invalid types: {error_dictionary}')

    def __str__(self):
        return str(self.columns_to_bounds)

    def exclude(self, columns=None):
        if columns == 'all':
            self.columns_to_bounds = {}
            return

        for attribute in columns:
            try:
                del self.columns_to_bounds[attribute]
            except:
                continue

    def schema_failure_temp_exclusion(self, columns):
        self._columns_to_bounds_temp = {}
        for attr in columns:
            self._columns_to_bounds_temp[attr] = self.columns_to_bounds.get(attr, None)
        
        self.exclude(columns=columns)

    def _undo_schema_failure_temp_exclusion(self):
        for column, settings in self._columns_to_bounds_temp.items():
            if settings != None:
                self.configure(columns=[column], lower_bound=settings['lower_bound'], upper_bound=settings['upper_bound'])
        self._columns_to_bounds_temp = {}

    def validate(self, dataframe_to_validate):
        import datetime

        if not self.columns_to_bounds or len(dataframe_to_validate) == 0:
            return {}

        data_to_return = {}
        for column, bounds in self.columns_to_bounds.items():
            data_to_return[column] = self._apply_min_max_test(column, dataframe_to_validate, bounds)

        self._undo_schema_failure_temp_exclusion()

        return data_to_return

    def _apply_min_max_test(self, column, dataframe_to_validate, bounds):

        attribute_data_type = dataframe_to_validate[column].dtype.kind

        min_value = dataframe_to_validate[column].min()
        max_value = dataframe_to_validate[column].max()

        min_max_test_result = {}

        if bounds['lower_bound'] is not None:
            min_max_test_result.update({
                'min_test': {
                    'lower_bound': bounds['lower_bound'],
                    'passed': min_value >= bounds['lower_bound'],
                    'min_value': min_value
                }
            })
        if bounds['upper_bound'] is not None:
            min_max_test_result.update({
                'max_test': {
                    'upper_bound': bounds['upper_bound'],
                    'passed': max_value <= bounds['upper_bound'],
                    'max_value': max_value
                }
            })

        if bounds['lower_bound'] and min_value < bounds['lower_bound']:
            min_max_test_result['min_test']['percentage_out_of_bounds'] = self._min_test_percentage(dataframe_to_validate, column, bounds['lower_bound'])
        if bounds['upper_bound'] and max_value > bounds['upper_bound']:
            min_max_test_result['max_test']['percentage_out_of_bounds'] = self._max_test_percentage(dataframe_to_validate, column, bounds['upper_bound'])

        return min_max_test_result

    @staticmethod
    def _min_test_percentage(dataframe_to_validate, column_name, lower_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] < lower_bound]) / len(dataframe_to_validate), 3)

    @staticmethod
    def _max_test_percentage(dataframe_to_validate, column_name, upper_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] > upper_bound]) / len(dataframe_to_validate), 3)
    