"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.range_parsers.datetime_range_parser import DateTimeRangeParser
from foundations_rest_api.range_parsers.elapsedtime_range_parser import ElapsedTimeRangeParser
from foundations_rest_api.range_parsers.status_range_parser import StatusRangeParser
from foundations_rest_api.range_parsers.string_range_parser import StringRangeParser


DATE_TIME, ELAPSED_TIME, STATUS, STRING = range(1, 4)


_column_type_parser = {
    DATE_TIME: DateTimeRangeParser,
    ELAPSED_TIME: ElapsedTimeRangeParser,
    STATUS: StatusRangeParser,
    STRING: StringRangeParser,
}


_column_type = {
    'duration': ELAPSED_TIME,
    'submitted_time': DATE_TIME,
    'start_time': DATE_TIME,
    'completed_time': DATE_TIME,
    'user': STRING,
    'status': STATUS,
}


def get_range_parser(column_name):
    return _column_type_parser[_column_type[column_name]]()
