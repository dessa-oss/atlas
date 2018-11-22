"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.api_filter_mixin import APIFilterMixin

class ExactMatchFilter(APIFilterMixin):

    def __call__(self, result, params):
        if result and isinstance(result, list):
            new_params = {key: value for key, value in params.items() if self._is_valid_column(result, key)}
            if new_params:
                self._filter(result, new_params)
        return result

    def _filter(self, result, params):
        for column_name, value in params.items():
            self._filter_column(result, column_name, value)

    def _filter_column(self, result, column_name, value):
        options = value.split(',')
        parsed_options = self._parse_options(column_name, options)
        if parsed_options:
            self._filter_exact_match(result, column_name, parsed_options)

    def _filter_exact_match(self, result, column_name, options):

        def column_value_in_options(item):
            value = getattr(item, column_name)
            return value in options

        return self._in_place_filter(column_value_in_options, result)

    def _parse_options(self, column_name, options):
        parser = self._get_parser(column_name)
        try:
            parsed_options = [parser.parse(option) for option in options]
        except ValueError:
            parsed_options = []
        return parsed_options
