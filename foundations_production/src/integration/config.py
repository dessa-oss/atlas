"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


integration_job_name = 'integration-job'

def _configure():
    from foundations_contrib.global_state import foundations_context
    from foundations_contrib.global_state import config_manager

    foundations_context.pipeline_context().file_name = integration_job_name
    config_manager['log_level'] = 'FATAL'

_configure()