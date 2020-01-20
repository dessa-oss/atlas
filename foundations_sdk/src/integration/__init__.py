"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from uuid import uuid4
import foundations
from foundations.global_state import redis_connection
import integration.config

from integration.test_pipeline_interface import TestPipelineInterface
from integration.test_log_param import TestLogParam