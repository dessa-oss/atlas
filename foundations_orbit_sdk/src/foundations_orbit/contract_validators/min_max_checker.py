"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MinMaxChecker(object):

    def __init__(self):
        self._attribute_and_bounds = {}

    def configure(self, attributes, lower_bound=None, upper_bound=None):
        if lower_bound is None and upper_bound is None:
            raise ValueError('expected either lower and/or upper bound')
        for attribute in attributes:
            self._attribute_and_bounds[attribute] = {
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
    
    def exclude(self, attributes=None):
        if attributes == 'all':
            self._attribute_and_bounds = {}
            return

        for attribute in attributes:
            del self._attribute_and_bounds[attribute]

    def validate(self, dataframe_to_validate):
        if not self._attribute_and_bounds or len(dataframe_to_validate) == 0:
            return {}

        data_to_return = {}

        for attribute, bounds in self._attribute_and_bounds.items():
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

        return data_to_return

    @staticmethod
    def _min_test_percentage(dataframe_to_validate, column_name, lower_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] < lower_bound]) / len(dataframe_to_validate), 3)

    @staticmethod
    def _max_test_percentage(dataframe_to_validate, column_name, upper_bound):
        return round(len(dataframe_to_validate[dataframe_to_validate[column_name] > upper_bound]) / len(dataframe_to_validate), 3)
    