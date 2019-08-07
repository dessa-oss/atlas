"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def indicate_model_ran_to_redis(job_id):
    from foundations_contrib.global_state import redis_connection
    redis_connection.incr(f'models:{job_id}:served')