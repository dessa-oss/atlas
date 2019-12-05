"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_core_rest_api_components.filters.api_filter_mixin import APIFilterMixin


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
            self._filter_column(result, column_name, value)

    def _filter_column(self, result, column_name, value):
        searched_value = self._enforce_safe_string(value)
        if searched_value:
            self._filter_contains(result, column_name, searched_value)

    def _filter_contains(self, result, column_name, searched_value):

        def column_value_in_options(item):
            column_value, item_parser = self._get_item_property_value_and_parser(item, column_name)
            if item_parser is None:
                return False
            value = self._enforce_safe_string(column_value)
            return searched_value.upper() in value.upper()

        return self._in_place_filter(column_value_in_options, result)

    def _enforce_safe_string(self, value):
        # TODO: Add some extra checking or sanitization
        if not isinstance(value, str):
            return str(value)
        return value
