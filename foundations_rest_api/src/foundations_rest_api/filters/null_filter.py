"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
from foundations_rest_api.filters.api_filter_mixin import APIFilterMixin


class NullFilter(APIFilterMixin):

    def __call__(self, result, params):
        if result and isinstance(result, list):
            new_params = {key: value for key, value in params.items() if key.endswith('_isnull')}
            if new_params:
                self._filter(result, new_params)
        return result

    def _filter(self, result, params):
        for key, param_value in params.items():
            column_name = key.split('_isnull', 1)[0]
            value = self._parse_value(param_value)
            if value is not None:
                self._filter_column(result, column_name, value)

    def _parse_value(self, param_value):
        from foundations_rest_api.filters.parsers import BoolParser

        parser = BoolParser()
        return parser.parse(param_value)

    def _filter_column(self, result, column_name, value):
        # Explicit is better than implicit [Zen of Python, 1]
        if value is True:
            self._filter_by_null_values(result, column_name)
        elif value is False:
            self._filter_by_not_null_values(result, column_name)

    def _is_none(self, value):
        return value is None or self._is_nan(value)

    def _is_nan(self, value):
        import math

        return isinstance(value, float) and math.isnan(value)

    def _filter_by_null_values(self, result, column_name):

        def column_value_is_null(item):
            value, item_parser = self._get_item_property_value_and_parser(item, column_name, parse=False)
            return item_parser is not None and self._is_none(value)

        return self._in_place_filter(column_value_is_null, result)

    def _filter_by_not_null_values(self, result, column_name):

        def column_value_is_not_null(item):
            value, item_parser = self._get_item_property_value_and_parser(item, column_name, parse=False)
            return item_parser is not None and not self._is_none(value)

        return self._in_place_filter(column_value_is_not_null, result)
