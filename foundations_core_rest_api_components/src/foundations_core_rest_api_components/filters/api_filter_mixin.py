"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""


class APIFilterMixin(object):

    def _is_valid_column(self, result, column_name):
        return hasattr(result[0], column_name)

    def _get_column_parser(self, column_name):
        from foundations_core_rest_api_components.filters.parsers import get_column_parser

        return get_column_parser(column_name)

    def _get_nested_element_parser(self, nested_element):
        from foundations_core_rest_api_components.filters.parsers import get_nested_element_parser

        element_type = nested_element.get('type', None)
        return get_nested_element_parser(element_type)

    def _in_place_filter(self, selection_function, result_list):
        for _ in range(len(result_list)):
            item = result_list.pop(0)
            if selection_function(item):
                result_list.append(item)

    def _get_item_property_value_and_parser(self, item, column_name, parse=True):

        if hasattr(item, column_name):
            return self._get_column_value_and_parser(item, column_name, parse)
        nested_element = self._find_element_in_parametric_properties(item, column_name)
        if nested_element:
            return self._get_nested_element_value_and_parser(nested_element, column_name, parse)
        return None, None  # column_name not found

    def _get_column_value_and_parser(self, item, column_name, parse=True):
        column_value = getattr(item, column_name)
        parser = self._get_column_parser(column_name)
        return parser.parse(column_value) if parse else column_value, parser

    def _get_nested_element_value_and_parser(self, nested_element, column_name, parse=True):
        column_value = nested_element.get('value', None)
        parser = self._get_nested_element_parser(nested_element)
        return parser.parse(column_value) if parse else column_value, parser

    def _find_element_in_parametric_properties(self, item, column_name):
        for parametric_property_name in ('input_params', 'output_metrics'):
            element = self._find_element_in_property(item, column_name, parametric_property_name)
            if element is not None:
                return element
        return None

    def _find_element_in_property(self, item, column_name, parametric_property_name):
        parametric_property = getattr(item, parametric_property_name, None)
        if parametric_property:
            element = self._search_property(column_name, parametric_property)
            if element is not None:
                return element
        return None

    def _search_property(self, column_name, parametric_property):
        for element in parametric_property:
            if element.get('name', None) == column_name:
                return element
        return None
