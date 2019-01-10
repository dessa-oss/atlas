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
        key {str} -- the name of the output metric.
        value {number, str, bool, array of [number|str|bool], array of array of [number|str|bool]} -- the value associated with the given output metric.

    Returns:
        - This function doesn't return a value.

    Raises:
        TypeError -- When a value of a non-supported type is provided as the metric value.

    Notes:
        A stage containing this function will not fail if the process of logging the metric fails for a
        reason that doesn't raise any exceptions.

    Example:
        ```python
        import foundations
        from algorithms import calculate_score

        def my_stage_code(self):
            score = calculate_score()
            foundations.log_metric('score', score)
        ```
    """
    stage_logging_context.log_metric(key, value)
