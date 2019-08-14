"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def track_production_metrics(metric_name, metric_values):
    import pickle
    from foundations_contrib.global_state import current_foundations_context, redis_connection

    try:
        job_id = current_foundations_context().job_id()

        metrics_list = list(metric_values.items())

        existing_metrics_from_redis = redis_connection.hmget(f'models:{job_id}:production_metrics', metric_name)[0]

        if existing_metrics_from_redis is None:
            existing_metrics = []
        else:
            existing_metrics = pickle.loads(existing_metrics_from_redis)
            
        metrics_to_store = existing_metrics + metrics_list

        redis_connection.hmset(f'models:{job_id}:production_metrics', {metric_name: pickle.dumps(metrics_to_store)})
    except ValueError:
        raise RuntimeError('Job ID not set')