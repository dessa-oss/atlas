"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.api_filter_mixin import APIFilterMixin


class ResultSorter(APIFilterMixin):

    def __call__(self, result, params):
        if result and 'sort' in params and isinstance(result, list):
            self._sort(result, params)
        return result

    def _sort(self, result, params):
        sort_param_value = params.get('sort')
        columns_specs_list = sort_param_value.split(',')
        self._sort_by_columns_specs_list(result, columns_specs_list)

    def _sort_by_columns_specs_list(self, result, columns_specs_list):
        columns_data_list = self._validate_columns(result, columns_specs_list)
        if columns_data_list:
            columns_data_list.reverse()
            for column_data in columns_data_list:
                self._sort_by_column_data(result, column_data)

    def _validate_columns(self, result, columns_specs_list):
        columns_data = []
        for column_spec in columns_specs_list:
            self._extract_valid_columns_data(columns_data, column_spec, result)
        return columns_data

    def _extract_valid_columns_data(self, columns_data, column_spec, result):
        column_spec = column_spec.strip()
        descending = column_spec.startswith('-')
        column_name = column_spec[1:] if descending else column_spec
        column_data = (descending, column_name)
        if self._is_valid_column(result, column_name):
            columns_data.append(column_data)

    def _sort_by_column_data(self, result, column_data):
        descending, column_name = column_data
        result.sort(reverse=descending, key=lambda item: self._custom_sorter_helper(item, column_name))

    def _custom_sorter_helper(self, item, column_name):
        val = getattr(item, column_name)
        if val:
            return val
        else:
            infinite_string = 'ZZZZ'
            return infinite_string + getattr(item, 'job_id')