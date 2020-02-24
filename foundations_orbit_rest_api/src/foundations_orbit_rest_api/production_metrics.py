
def all_production_metrics(project_name, monitor_name):
    all_items = _serialized_items_from_redis(_redis_key(project_name, monitor_name))
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

def _redis_key(project_name, monitor_name):
    return f'projects:{project_name}:monitors:{monitor_name}:production_metrics'
