
import foundations
import json

from foundations_contrib.global_state import current_foundations_job

params = foundations.load_parameters()
print(current_foundations_job().job_id)
print(json.dumps(params))