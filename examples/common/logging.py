"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def log_data(data):
    _log().info(repr(data))
    return data

def log_formatted(format_string, *args):
    _log().info(format_string.format(*args))
    return list(args)

def _log():
    from foundations import log_manager
    return log_manager.get_logger(__name__)
