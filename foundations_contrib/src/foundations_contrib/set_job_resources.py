"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.global_state import current_foundations_context
from foundations_internal.job_resources import JobResources

def set_job_resources(num_gpus, ram):
    if ram <= 0:
        raise ValueError('Invalid RAM quantity. Please provide a RAM quantity greater than zero.')

    job_resources = JobResources(num_gpus, ram)
    current_foundations_context().set_job_resources(job_resources)
