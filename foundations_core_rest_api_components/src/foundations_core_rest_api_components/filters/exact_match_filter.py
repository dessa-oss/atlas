"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_core_rest_api_components.filters.api_filter_mixin import APIFilterMixin


class ExactMatchFilter(APIFilterMixin):

    def __init__(self):
        self._parsing_state = {}

    def __call__(self, result, params):
        if result and isinstance(result, list):
            self._filter(result, params)
        return result

    def _filter(self, result, params):
        for column_name, value in params.items():
            self._filter_column(result, column_name, value)

    def _filter_column(self, result, column_name, value):
        options = value.split(',')
        self._parsing_state[column_name] = {'parser': None, 'options': options}
        if options:
            self._filter_exact_match(result, column_name, options)

    def _filter_exact_match(self, result, column_name, options):

        def column_value_in_options(item):
            value, item_parser = self._get_item_property_value_and_parser(item, column_name)
            if item_parser is None:
                return False
            parsed_options = self._get_parsed_options(column_name, options, item_parser)
            return value in parsed_options

        return self._in_place_filter(column_value_in_options, result)

    def _get_parsed_options(self, column_name, options, new_parser):
        self._update_parsing_state(column_name, options, new_parser)
        return self._parsing_state[column_name]['options']

    def _update_parsing_state(self, column_name, options, new_parser):
        if not isinstance(new_parser, type(self._parsing_state[column_name]['parser'])):
            parsed_options = self._parse_options(options, new_parser)
            self._parsing_state[column_name]['parser'] = new_parser
            self._parsing_state[column_name]['options'] = parsed_options

    def _parse_options(self, options, parser):
        try:
            parsed_options = [parser.parse(option) for option in options]
        except ValueError:
            parsed_options = []
        return parsed_options
