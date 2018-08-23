"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.null_stage_logger import NullStageLogger
from foundations.stage_logging_context import StageLoggingContext

stage_logging_context = StageLoggingContext(NullStageLogger())

def log_metric(key, value):
    stage_logging_context.log_metric(key, value)