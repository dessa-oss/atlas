"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class APIFilterMixin(object):

    def _is_valid_column(self, result, column_name):
        return hasattr(result[0], column_name)

    def _get_parser(self, column_name):
        from foundations_rest_api.filters.parsers import get_parser

        return get_parser(column_name)

    def _in_place_filter(self, selection_function, result_list):
        for _ in range(len(result_list)):
            item = result_list.pop(0)
            if selection_function(item):
                result_list.append(item)
