"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class APIFilter(object):

    def __call__(self, result, params):
        if result and isinstance(result, list):
            new_params = {key: value for key, value in params.items() if key.startswith('start_') or key.startswith('end_')}
            if new_params:
                self._filter_by(result, new_params)
        return result

    def _filter_by(self, result, params):
        columns_filtering_data = self._get_columns_filtering_data(result, params)
        for column_name, start_param_value, end_param_value in columns_filtering_data:
            self._do_filtering(result, column_name, start_param_value, end_param_value)

    def _get_columns_filtering_data(self, result, params):
        columns_filtering_data = []
        start_keys = [key for key in params.keys() if key.startswith('start_')]
        while start_keys and params:
            self._extract_columns_filtering_data(result, start_keys, params, columns_filtering_data)
        return columns_filtering_data

    def _extract_columns_filtering_data(self, result, start_keys, params, columns_filtering_data):
        start_key = start_keys.pop(0)
        column_name = start_key.split('start_', 1)[1]
        if self._is_column_valid(result, column_name):
            self._populate_column_filtering_data(start_key, column_name, params, columns_filtering_data)

    def _populate_column_filtering_data(self, start_key, column_name, params, columns_filtering_data):
        start_param_value = params.pop(start_key, None)
        end_key = '_'.join(['end', column_name])
        end_param_value = params.pop(end_key, None)
        if column_name and start_param_value and end_param_value:
            columns_filtering_data.append((column_name, start_param_value, end_param_value))

    def _do_filtering(self, result, column_name, start_param_value, end_param_value):
        range_parser = self._get_range_parser(column_name)
        if range_parser.is_valid_range(start_param_value, end_param_value):
            start_value, end_value = range_parser.parse(start_param_value, end_param_value)
            self._filter_by_range(result, column_name, start_value, end_value)

    def _filter_by_range(self, result, column_name, start_value, end_value):

        def is_in_range(item):
            value = getattr(item, column_name)
            return value >= start_value and value <= end_value

        return filter(is_in_range, result)

    def _is_column_valid(self, result, column_name):
        return hasattr(result[0], column_name)

    def _get_range_parser(self, column_name):
        from foundations_rest_api.range_parsers import get_range_parser

        return get_range_parser(column_name)
