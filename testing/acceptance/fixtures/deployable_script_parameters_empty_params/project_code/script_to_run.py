"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
import json

from foundations_contrib.global_state import current_foundations_context

params = foundations.load_parameters()
print(current_foundations_context().job_id())
print(json.dumps(params))