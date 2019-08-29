"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def all_production_metrics(job_id):
    all_items = _serialized_items_from_redis(_redis_key())
    return {_decoded_metric_name(metric_name): _deserialized_metric_values(metric_values) for metric_name, metric_values in all_items}

def _decoded_metric_name(metric_name):
    return metric_name.decode()

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
