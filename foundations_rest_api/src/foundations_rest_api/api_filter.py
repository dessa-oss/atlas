"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class APIFilter(object):

    def __call__(self, result, params):
        if result and 'filter_by' in params and isinstance(result, list):
            self._filer_by(result, params)
        return result

    def _filer_by(self, result, params):
        column_name = params.get('filter_by', None)
        starts_param_value, ends_param_value = self._get_range_values(params)
        if column_name and starts_param_value and ends_param_value:
            self._start_filtering(result, column_name, starts_param_value, ends_param_value)

    def _start_filtering(self, result, column_name, starts_param_value, ends_param_value):
        if self._is_column_valid(result, column_name):
            self._do_filtering(result, column_name, starts_param_value, ends_param_value)

    def _do_filtering(self, result, column_name, starts_param_value, ends_param_value):
        range_parser = self._get_range_parser(column_name)
        if range_parser.is_valid_range(starts_param_value, ends_param_value):
            start_value, end_value = range_parser.parse(starts_param_value, ends_param_value)
            self._filter_by_range(result, column_name, start_value, end_value)

    def _filter_by_range(self, result, column_name, start_value, end_value):

        def is_in_range(item):
            value = getattr(item, column_name)
            return value >= start_value and value <= end_value

        return filter(is_in_range, result)

    def _get_range_values(self, params):
        starts_param_value = params.get('filter_starts', None)
        ends_param_value = params.get('filter_ends', None)
        return starts_param_value, ends_param_value

    def _is_column_valid(self, result, column_name):
        return hasattr(result[0], column_name)


    def _get_range_parser(self, column_name):
        from foundations_rest_api.range_parsers import get_range_parser

        return get_range_parser(column_name)
