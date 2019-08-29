"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _redis_key():
    import os
    job_id = os.environ['JOB_ID']
    return f'models:{job_id}:production_metrics'

def all_production_metrics(job_id):
    from foundations_contrib.global_state import redis_connection
    all_items = list(redis_connection.hgetall(_redis_key()).items())
    if not all_items:
        return {}
    metric_name, metric_values = all_items[0]
    return {metric_name.decode(): []}
