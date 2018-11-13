"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class ResultSorter(object):

    def __call__(self, result, params):
        print('1.-', result)
        print('2.-', params)
        if result and 'sort' in params and isinstance(result, list):
            sort_param_value = params.get('sort')
            columns_spec_list = sort_param_value.split(',')
            self._sort(result, columns_spec_list)
        return result

    def _sort(self, result, columns_spec_list):
        columns = self._validate_columns(result, columns_spec_list)
        print('===>', columns)
        if columns:
            columns.reverse()
            for column in columns:
                result.sort(reverse=column[0], key=lambda x: getattr(x, column[1]))

    def _validate_columns(self, result, columns_spec_list):
        columns = []
        for column_spec in columns_spec_list:
            column_spec = column_spec.strip()
            column_data = (column_spec.startswith('-'), column_spec[1:])
            if hasattr(result[0], column_data[1]):
                columns.append(column_data)
        return columns
