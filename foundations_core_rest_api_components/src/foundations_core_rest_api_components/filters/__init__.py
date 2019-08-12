
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_core_rest_api_components.filters.result_sorter import ResultSorter
from foundations_core_rest_api_components.filters.range_filter import RangeFilter
from foundations_core_rest_api_components.filters.exact_match_filter import ExactMatchFilter
from foundations_core_rest_api_components.filters.contains_filter import ContainsFilter
from foundations_core_rest_api_components.filters.null_filter import NullFilter


_result_filters = {'sort': ResultSorter(),
                   'starts': RangeFilter(),
                   'contains': ContainsFilter(),
                   'isnull': NullFilter()}


def get_api_filters(filter_detection_key):
    if filter_detection_key == 'ends':
        filter_detection_key = 'starts'
    return _result_filters.get(filter_detection_key, ExactMatchFilter())
