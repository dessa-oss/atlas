
import foundations
import json

from foundations_contrib.global_state import current_foundations_context

params = foundations.load_parameters()
print(current_foundations_context().job_id)
print(json.dumps(params))