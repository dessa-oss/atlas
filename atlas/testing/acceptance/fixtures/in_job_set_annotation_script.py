
import os

import foundations
from foundations_contrib.global_state import current_foundations_job, message_router
from foundations_events.producers.jobs import RunJob

foundations.set_project_name('default')

job_id = os.environ['ACCEPTANCE_TEST_JOB_ID']
current_foundations_job().job_id = job_id

RunJob(message_router, current_foundations_job()).push_message()

foundations.set_tag('model type', 'simple mlp')
foundations.set_tag('data set', 'out of time')
foundations.set_tag('what I was doing,', 'drinking tea')

print('Hello World!')