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
    Generate output metrics for the stage where it is called.

    Arguments:
        key {string} -- the name of the output metric.
        value {any type} -- the value associated with the given output metric.
    """
    stage_logging_context.log_metric(key, value)
