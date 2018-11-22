"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.api_filter_mixin import APIFilterMixin

class ContainsFilter(APIFilterMixin):

    def __call__(self, result, params):
        if result and isinstance(result, list):
            new_params = {key: value for key, value in params.items() if key.endswith('_contains')}
            if new_params:
                self._filter(result, new_params)
        return result

    def _filter(self, result, params):
        for key, value in params.items():
            column_name = key.split('_contains', 1)[0]
            if self._is_valid_column(result, column_name):
                self._filter_column(result, column_name, value)

    def _filter_column(self, result, column_name, value):
        sanitized_value = self._parse_value(value)
        if sanitized_value:
            self._filter_contains(result, column_name, sanitized_value)

    def _filter_contains(self, result, column_name, searched_value):

        def column_value_in_options(item):
            value = getattr(item, column_name)
            return searched_value in value if isinstance(value, str) else False

        return self._in_place_filter(column_value_in_options, result)

    def _parse_value(self, value):
        from foundations_rest_api.filters.parsers import StringParser

        parser = StringParser()
        try:
            sanitized_value = parser.parse(value)
        except ValueError:
            sanitized_value = None
        return sanitized_value
