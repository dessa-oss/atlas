"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.api_filter_mixin import APIFilterMixin

class RangeFilter(APIFilterMixin):

    def __call__(self, result, params):
        if result and isinstance(result, list):
            new_params = {key: value for key, value in params.items() if key.endswith('_starts') or key.endswith('_ends')}
            if new_params:
                self._filter(result, new_params)
        return result

    def _filter(self, result, params):
        columns_filtering_data = self._get_columns_filtering_data(result, params)
        for column_name, start_param_value, end_param_value in columns_filtering_data:
            self._do_filtering(result, column_name, start_param_value, end_param_value)

    def _get_columns_filtering_data(self, result, params):
        columns_filtering_data = []
        start_keys = [key for key in params.keys() if key.endswith('_starts')]
        while start_keys and params:
            self._extract_columns_filtering_data(result, start_keys, params, columns_filtering_data)
        return columns_filtering_data

    def _extract_columns_filtering_data(self, result, start_keys, params, columns_filtering_data):
        start_key = start_keys.pop(0)
        column_name = start_key.split('_starts', 1)[1]
        if self._is_valid_column(result, column_name):
            self._populate_column_filtering_data(start_key, column_name, params, columns_filtering_data)

    def _populate_column_filtering_data(self, start_key, column_name, params, columns_filtering_data):
        start_param_value = params.pop(start_key, None)
        end_key = '_'.join([column_name, 'ends'])
        end_param_value = params.pop(end_key, None)
        if column_name and start_param_value and end_param_value:
            columns_filtering_data.append((column_name, start_param_value, end_param_value))

    def _do_filtering(self, result, column_name, start_param_value, end_param_value):
        start_value, end_value = self._parse_range_param_values(column_name, start_param_value, end_param_value)
        if self._is_valid_range(start_value, end_value):
            self._filter_by_range(result, column_name, start_value, end_value)

    def _parse_range_param_values(self, column_name, start_param_value, end_param_value):
        parser = self._get_parser(column_name)
        try:
            start_value = parser.parse(start_param_value)
            end_value = parser.parse(end_param_value)
        except ValueError:
            start_value = None
            end_value = None
        return start_value, end_value

    def _is_valid_range(self, start_value, end_value):
        return start_value is not None and end_value is not None and end_value >= start_value

    def _filter_by_range(self, result, column_name, start_value, end_value):

        def is_in_range(item):
            value = getattr(item, column_name)
            return value >= start_value and value <= end_value

        return filter(is_in_range, result)

    def _get_parser(self, column_name):
        from foundations_rest_api.filters.parsers import get_parser

        return get_parser(column_name)
