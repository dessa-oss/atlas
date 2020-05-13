
class GlobalMetricLogger(object):

    def __init__(self, message_router):
        self._message_router = message_router
    
    def log_metric(self, key, value):
        from foundations_contrib.global_state import log_manager
        from foundations_events.producers.metric_logged import MetricLogged

        if self._is_job_running():
            metric_logged_producer = MetricLogged(self._message_router, self._project_name(), self._job_id(), key, value)
            metric_logged_producer.push_message()
        elif not log_manager.foundations_not_running_warning_printed():
            logger = log_manager.get_logger(__name__)
            logger.warning('Script not run with Foundations.')
            log_manager.set_foundations_not_running_warning_printed()

    def _is_job_running(self):
        return self._foundations_context.is_in_running_job()

    def _project_name(self):
        return self._foundations_context.project_name

    def _job_id(self):
        return self._foundations_context.job_id

    @property
    def _foundations_context(self):
        from foundations_contrib.global_state import current_foundations_job
        return current_foundations_job()

def global_metric_logger_for_job():
    from foundations_contrib.global_state import message_router
    return GlobalMetricLogger(message_router)