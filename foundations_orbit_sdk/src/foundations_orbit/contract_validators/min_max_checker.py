"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_orbit.contract_validators.checker import Checker
class MinMaxChecker(object):

    def __init__(self, reference_column_types):
        self._attribute_and_bounds = {}
        self._reference_column_types = reference_column_types
        self._allowed_types = ['int', 'float', 'datetime']
        self._attributes_not_allowed = Checker.find_invalid_attributes(self._allowed_types, self._reference_column_types)
        self.attributes_and_bounds_temp = {}

    def configure(self, attributes, lower_bound=None, upper_bound=None):
        error_dictionary = {}
        if lower_bound is None and upper_bound is None:
            raise ValueError('expected either lower and/or upper bound')
        for attribute in attributes:
            if attribute in self._attributes_not_allowed:
                error_dictionary[attribute] = self._reference_column_types[attribute]
            else:
                self._attribute_and_bounds[attribute] = {
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        if error_dictionary != {}:
            self._attribute_and_bounds = {}
            raise ValueError(f'The following columns have invalid types: {error_dictionary}')

    def __str__(self):
        return str(self._attribute_and_bounds)

    def exclude(self, attributes=None):
        if attributes == 'all':
            self._attribute_and_bounds = {}
            return

        for attribute in attributes:
            try:
                del self._attribute_and_bounds[attribute]
            except:
                continue

    def temp_exclude(self, attributes):
        self.attributes_and_bounds_temp = {}
        for attr in attributes:
            self.attributes_and_bounds_temp[attr] = self._attribute_and_bounds.get(attr, None)
        
        self.exclude(attributes=attributes)

    def validate(self, dataframe_to_validate):
        import datetime

        if not self._attribute_and_bounds or len(dataframe_to_validate) == 0:
            return {}

        data_to_return = {}
        for attribute, bounds in self._attribute_and_bounds.items():

            attribute_data_type = dataframe_to_validate[attribute].dtype.kind

            min_value = dataframe_to_validate[attribute].min()
            max_value = dataframe_to_validate[attribute].max()

            data_to_return[attribute] = {}

            if bounds['lower_bound'] is not None:
                data_to_return[attribute].update({
                    'min_test': {
                        'lower_bound': bounds['lower_bound'],
                        'passed': min_value >= bounds['lower_bound'],
                        'min_value': min_value
                    }
                })
            if bounds['upper_bound'] is not None:
                data_to_return[attribute].update({
                    'max_test': {
                        'upper_bound': bounds['upper_bound'],
                        'passed': max_value <= bounds['upper_bound'],
                        'max_value': max_value
                    }
                })

            if bounds['lower_bound'] and min_value < bounds['lower_bound']:
                data_to_return[attribute]['min_test']['percentage_out_of_bounds'] = self._min_test_percentage(dataframe_to_validate, attribute, bounds['lower_bound'])
            if bounds['upper_bound'] and max_value > bounds['upper_bound']:
                data_to_return[attribute]['max_test']['percentage_out_of_bounds'] = self._max_test_percentage(dataframe_to_validate, attribute, bounds['upper_bound'])

        for attribute, settings in self.attributes_and_bounds_temp.items():
            if settings != None:
                self.configure(attributes=[attribute], lower_bound=settings['lower_bound'], upper_bound=settings['upper_bound'])
        self.attributes_and_bounds_temp = {}

        return data_to_return

    @staticmethod
    def _min_test_percentage(dataframe_to_validate, column_name, lower_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] < lower_bound]) / len(dataframe_to_validate), 3)

    @staticmethod
    def _max_test_percentage(dataframe_to_validate, column_name, upper_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] > upper_bound]) / len(dataframe_to_validate), 3)
    