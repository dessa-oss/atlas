"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""


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
    from foundations_contrib.global_state import log_manager, message_router, current_foundations_context
    from foundations_contrib.producers.metric_logged import MetricLogged
    from foundations_contrib.utils import is_job_running

    pipeline_context = current_foundations_context().pipeline_context()
    project_name = pipeline_context.provenance.project_name

    if is_job_running(pipeline_context):
        job_id = pipeline_context.file_name
        metric_logged_producer = MetricLogged(message_router, project_name, job_id, key, value)
        metric_logged_producer.push_message()
    elif not log_manager.foundations_not_running_warning_printed():
        logger = log_manager.get_logger(__name__)
        logger.warning('Script not run with Foundations.')
        log_manager.set_foundations_not_running_warning_printed()


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