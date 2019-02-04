"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.parsers.datetime_parser import DateTimeParser
from foundations_rest_api.filters.parsers.elapsed_time_parser import ElapsedTimeParser
from foundations_rest_api.filters.parsers.status_parser import StatusParser
from foundations_rest_api.filters.parsers.string_parser import StringParser
from foundations_rest_api.filters.parsers.number_parser import NumberParser
from foundations_rest_api.filters.parsers.bool_parser import BoolParser


column_parser_types = {
    'job_id': StringParser,
    'submitted_time': DateTimeParser,
    'start_time': DateTimeParser,
    'completed_time': DateTimeParser,
    'user': StringParser,
    'status': StatusParser,
    'duration': ElapsedTimeParser
}


nested_parser_types = {
    'number': NumberParser,
    'bool': BoolParser
}


def get_column_parser(column_name):
    return column_parser_types.get(column_name, StringParser)()


def get_nested_element_parser(nested_element_type):
    return nested_parser_types.get(nested_element_type, StringParser)()
