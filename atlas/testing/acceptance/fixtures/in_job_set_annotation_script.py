
import os

import foundations
from foundations_contrib.global_state import current_foundations_context, message_router
from foundations_events.producers.jobs import RunJob

foundations.set_project_name('default')

job_id = os.environ['ACCEPTANCE_TEST_JOB_ID']
pipeline_context = current_foundations_context().pipeline_context()
pipeline_context.file_name = job_id

RunJob(message_router, pipeline_context).push_message()

foundations.set_tag('model type', 'simple mlp')
foundations.set_tag('data set', 'out of time')
foundations.set_tag('what I was doing,', 'drinking tea')

print('Hello World!')