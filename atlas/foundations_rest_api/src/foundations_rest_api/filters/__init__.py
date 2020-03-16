
from foundations_rest_api.filters.result_sorter import ResultSorter
from foundations_rest_api.filters.range_filter import RangeFilter
from foundations_rest_api.filters.exact_match_filter import ExactMatchFilter
from foundations_rest_api.filters.contains_filter import ContainsFilter
from foundations_rest_api.filters.null_filter import NullFilter


_result_filters = {'sort': ResultSorter(),
                   'starts': RangeFilter(),
                   'contains': ContainsFilter(),
                   'isnull': NullFilter()}


def get_api_filters(filter_detection_key):
    if filter_detection_key == 'ends':
        filter_detection_key = 'starts'
    return _result_filters.get(filter_detection_key, ExactMatchFilter())
