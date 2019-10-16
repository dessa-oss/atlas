"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MinMaxChecker(object):

    def __init__(self):
        self._attributes = None

    def configure(self, attributes, lower_bound=None, upper_bound=None):
        if lower_bound is None and upper_bound is None:
            raise ValueError('expected either lower and/or upper bound')
        self._attributes = attributes
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def validate(self, dataframe_to_validate):
        if not self._attributes or len(dataframe_to_validate) == 0:
            return {}

        min_value = dataframe_to_validate[self._attributes[0]].min()

        if self._lower_bound:
            data_to_return = {
                self._attributes[0]: {
                    'min_test': {
                        'lower_bound': self._lower_bound,
                        'passed': min_value >= self._lower_bound,
                        'min_value': min_value
                    }
                }
            }
        else:
            data_to_return = {
                self._attributes[0]: {
                    'max_test': {
                        'upper_bound': self._upper_bound,
                        'passed': True,
                        'max_value': 110
                    }
                }
            }

        if self._lower_bound and min_value < self._lower_bound:
            data_to_return[self._attributes[0]]['min_test']['percentage_out_of_bounds'] = self._min_test_percentage(dataframe_to_validate, self._attributes[0], self._lower_bound)

        return data_to_return

    @staticmethod
    def _min_test_percentage(dataframe_to_validate, column_name, lower_bound):
        return len(dataframe_to_validate[dataframe_to_validate[column_name] < lower_bound]) / len(dataframe_to_validate)
    