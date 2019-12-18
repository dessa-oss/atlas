"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def track_production_metrics(metric_name, metric_values):
    _track_production_metrics_for_job(_redis_key(), metric_name, metric_values)

def _track_production_metrics_for_job(redis_key, metric_name, metric_values):
    import functools
    import pickle
    from foundations_contrib.global_state import redis_connection

    type_normalizer = functools.partial(_metric_pair_with_normalized_type, metric_name)

    metrics_list = list(map(type_normalizer, metric_values.items()))

    existing_metrics = _existing_metrics_from_redis(redis_key, metric_name)
    metrics_to_store = existing_metrics + metrics_list

    metrics = {metric_name: pickle.dumps(metrics_to_store)}

    redis_connection.hmset(redis_key, metrics)

def _metric_pair_with_normalized_type(metric_name, key_value_pair):
    column_name, column_value = key_value_pair
    normalized_value = _with_normalized_type(column_value)

    if normalized_value is None:
        error_message = f'cannot log metric `{metric_name}` with column name `{column_name}` of type `{type(column_value)}` - must be able to cast to int or float'
        raise TypeError(error_message)

    return (column_name, normalized_value)

def _with_normalized_type(value):
    as_int = _try_cast(value, int)
    as_float = _try_cast(value, float)

    if as_int is None:
        return as_float if as_float is not None else None
    elif as_float is None:
        return as_int
    else:
        return as_int if as_int == as_float else as_float

def _try_cast(value, target_class):
    try:
        return target_class(value)
    except (ValueError, TypeError):
        return None

def _existing_metrics_from_redis(redis_key, metric_name):
    import pickle
    from foundations_contrib.global_state import redis_connection

    existing_metrics_from_redis = redis_connection.hmget(redis_key, metric_name)[0]

    if existing_metrics_from_redis is None:
        return []

    return pickle.loads(existing_metrics_from_redis)

def _redis_key():
    import os

    monitor_name = os.environ['MONITOR_NAME']
    project_name = os.environ['PROJECT_NAME']

    if not monitor_name:
        raise RuntimeError('Monitor name not set')
    if not project_name:
        raise RuntimeError('Project name not set')
    
    return f'projects:{project_name}:monitors:{monitor_name}:production_metrics'