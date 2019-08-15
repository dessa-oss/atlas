"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def track_production_metrics(metric_name, metric_values):
    try:
        _track_production_metrics_for_job(_redis_key(), metric_name, metric_values)
    except ValueError:
        raise RuntimeError('Job ID not set')

def _track_production_metrics_for_job(redis_key, metric_name, metric_values):
    import pickle
    from foundations_contrib.global_state import redis_connection

    metrics_list = list(metric_values.items())

    existing_metrics = _existing_metrics_from_redis(redis_key, metric_name)
    metrics_to_store = existing_metrics + metrics_list

    metrics = {metric_name: pickle.dumps(metrics_to_store)}

    redis_connection.hmset(redis_key, metrics)

def _existing_metrics_from_redis(redis_key, metric_name):
    import pickle
    from foundations_contrib.global_state import redis_connection

    existing_metrics_from_redis = redis_connection.hmget(redis_key, metric_name)[0]

    if existing_metrics_from_redis is None:
        return []

    return pickle.loads(existing_metrics_from_redis)

def _redis_key():
    import os

    job_id = os.environ['JOB_ID']

    if not job_id:
        raise ValueError()
    return f'models:{job_id}:production_metrics'