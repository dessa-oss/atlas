

def log_metric(key, value):
    from foundations.utils import is_string

    if not is_string(key):
        raise ValueError('Invalid metric name `{}`'.format(key))

    if _is_scalar_loggable(value):
        _log_metric(key, value)
    elif _is_list_loggable(value):
        for metric in value:
            _log_metric(key, metric)
    else:
        error_message = 'Invalid metric with key="{}" of value={} with type {}. Value should be of type string or ' \
                        'number, or a list of strings / numbers'
        string_representation = _get_string_representation(value)
        raise TypeError(error_message.format(key, string_representation, type(value)))


def _log_metric(key, value):
    from foundations.utils import log_warning_if_not_running_in_job
    log_warning_if_not_running_in_job(_log_metric_in_running_job, key, value)


def _log_metric_in_running_job(key, value):
    from foundations_contrib.global_state import message_router, current_foundations_job
    from foundations_events.producers.metric_logged import MetricLogged

    project_name = current_foundations_job().project_name
    job_id = current_foundations_job().job_id

    metric_logged_producer = MetricLogged(message_router, project_name, job_id, key, value)
    metric_logged_producer.push_message()


def _is_list_loggable(value):
    if isinstance(value, list):
        check_for_loggable_elements = map(_is_scalar_loggable, value)
        return all(check_for_loggable_elements)

    return False


def _is_scalar_loggable(value):
    from foundations.utils import is_string, is_number
    return is_string(value) or is_number(value)


def _get_string_representation(value):
    representation = str(value)

    if len(representation) > 30:
        representation = representation[:30] + " ..."
    
    return representation