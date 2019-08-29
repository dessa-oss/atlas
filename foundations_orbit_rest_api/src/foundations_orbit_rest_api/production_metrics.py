"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def all_production_metrics(job_id):
    all_items = _serialized_items_from_redis(_redis_key())
    
    if not all_items:
        return {}
    
    metric_name, metric_values = all_items[0]
    deserialized_metric_values = _deserialized_metric_values(metric_values)

    if deserialized_metric_values:
        deserialized_metric_values = [deserialized_metric_values[0]]

    return {metric_name.decode(): deserialized_metric_values}

def _deserialized_metric_values(metric_values):
    import pickle
    return pickle.loads(metric_values)

def _serialized_items_from_redis(key):
    from foundations_contrib.global_state import redis_connection
    items_iterator = redis_connection.hgetall(key).items()
    return list(items_iterator)

def _redis_key():
    import os
    job_id = os.environ['JOB_ID']
    return f'models:{job_id}:production_metrics'
