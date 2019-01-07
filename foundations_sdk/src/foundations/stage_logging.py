"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.null_stage_logger import NullStageLogger
from foundations_internal.stage_logging_context import StageLoggingContext

stage_logging_context = StageLoggingContext(NullStageLogger())


def log_metric(key, value):
    """
    Log metrics within a stage from where it is called.

    Arguments:
        key {string} -- the name of the output metric.
        value {number, str, bool, array of base types, array of array of base types} -- the value associated with the given output metric.

    Returns:
        - This function doesn't return a value.

    Raises:
        TypeError -- When a value of a non-supported type is provided as the metric value.

    Notes:
        A stage containing this function won't fail if this function fails.
    """
    stage_logging_context.log_metric(key, value)
