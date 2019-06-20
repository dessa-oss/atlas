"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""

import os

import foundations
import foundations.prototype
from foundations_contrib.global_state import current_foundations_context, message_router
from foundations_contrib.producers.jobs.run_job import RunJob

foundations.set_project_name('default')

job_id = os.environ['ACCEPTANCE_TEST_JOB_ID']
pipeline_context = current_foundations_context().pipeline_context()
pipeline_context.file_name = job_id

RunJob(message_router, pipeline_context).push_message()

foundations.prototype.set_tag('model type', 'simple mlp')

print('Hello World!')