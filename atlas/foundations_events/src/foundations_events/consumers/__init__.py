
from foundations_contrib.global_state import message_router, config_manager
from foundations_events.notifiers import SlackNotifier
from foundations_events.notifiers import JobNotifier

_add_listener = message_router.add_listener
_job_notifier = JobNotifier(config_manager, SlackNotifier())


def _add_consumers_for_metrics(redis):
    from foundations_events.consumers.job_metric_consumer import JobMetricConsumer
    from foundations_events.consumers.job_metric_name_consumer import JobMetricNameConsumer
    from foundations_events.consumers.project_metrics import ProjectMetrics
    from foundations_events.consumers.single_project_metric import SingleProjectMetric

    _add_listener(JobMetricConsumer(redis), 'job_metrics')
    _add_listener(JobMetricNameConsumer(redis), 'job_metrics')
    _add_listener(ProjectMetrics(redis), 'job_metrics')
    _add_listener(SingleProjectMetric(redis), 'job_metrics')


def _add_consumers_for_job_annotations(redis):
    from foundations_events.consumers.annotate import Annotate

    annotation_consumer = Annotate(redis)
    _add_listener(annotation_consumer, 'job_tag')


def _add_consumers_for_queue_job(redis):
    from foundations_events.consumers.jobs.queued.creation_time import CreationTime
    from foundations_events.consumers.jobs.queued.job_state import JobState
    from foundations_events.consumers.jobs.queued.project_listing_for_queued_job import ProjectListingForQueuedJob
    from foundations_events.consumers.jobs.queued.global_listing import GlobalListing
    from foundations_events.consumers.jobs.queued.project_name import ProjectName
    from foundations_events.consumers.jobs.queued.run_data_keys import RunDataKeys
    from foundations_events.consumers.jobs.queued.run_data import RunData
    from foundations_events.consumers.jobs.queued.set_user import SetUser
    from foundations_events.consumers.jobs.queued.project_tracker import ProjectTracker
    from foundations_events.consumers.jobs.queued.job_notifier import JobNotifier
    from foundations_events.consumers.jobs.queued.project_listing import ProjectListing

    import json

    _add_listener(CreationTime(redis), 'queue_job')
    _add_listener(JobState(redis), 'queue_job')
    _add_listener(ProjectListingForQueuedJob(redis), 'queue_job')
    _add_listener(GlobalListing(redis), 'queue_job')
    _add_listener(ProjectName(redis), 'queue_job')
    _add_listener(RunDataKeys(redis), 'queue_job')
    _add_listener(RunData(redis, json), 'queue_job')
    _add_listener(SetUser(redis), 'queue_job')
    _add_listener(ProjectTracker(redis), 'queue_job')
    _add_listener(JobNotifier(_job_notifier), 'queue_job')
    _add_listener(ProjectListing(redis), 'queue_job')


def _add_consumers_for_run_job(redis):
    from foundations_events.consumers.jobs.running.job_state import JobState
    from foundations_events.consumers.jobs.running.remove_queued_job import RemoveQueuedJob
    from foundations_events.consumers.jobs.running.remove_global_queued_job import RemoveGlobalQueuedJob
    from foundations_events.consumers.jobs.running.start_time import StartTime
    from foundations_events.consumers.jobs.running.job_notifier import JobNotifier
    from foundations_events.consumers.jobs.running.monitor_name import MonitorName

    _add_listener(JobState(redis), 'run_job')
    _add_listener(RemoveQueuedJob(redis), 'run_job')
    _add_listener(RemoveGlobalQueuedJob(redis), 'run_job')
    _add_listener(StartTime(redis), 'run_job')
    _add_listener(JobNotifier(_job_notifier), 'run_job')


def _add_consumers_for_complete_job(redis):
    from foundations_events.consumers.jobs.completed.completed_time import CompletedTime
    from foundations_events.consumers.jobs.completed.job_state import JobState
    from foundations_events.consumers.jobs.completed.job_notifier import JobNotifier
    from foundations_events.consumers.jobs.completed.global_listing import GlobalListing

    _add_listener(CompletedTime(redis), 'complete_job')
    _add_listener(JobState(redis), 'complete_job')
    _add_listener(GlobalListing(redis), 'complete_job')
    _add_listener(JobNotifier(_job_notifier), 'complete_job')


def _add_consumers_for_fail_job(redis):
    from foundations_events.consumers.jobs.completed.completed_time import CompletedTime
    from foundations_events.consumers.jobs.failed.error_data import ErrorData
    from foundations_events.consumers.jobs.failed.job_state import JobState
    from foundations_events.consumers.jobs.failed.job_notifier import JobNotifier
    import json

    _add_listener(CompletedTime(redis), 'fail_job')
    _add_listener(ErrorData(redis, json), 'fail_job')
    _add_listener(JobState(redis), 'fail_job')
    _add_listener(JobNotifier(_job_notifier), 'fail_job')


def _create_redis_instance_and_add_consumers():
    from foundations_contrib.global_state import redis_connection

    _add_consumers_for_metrics(redis_connection)
    _add_consumers_for_queue_job(redis_connection)
    _add_consumers_for_run_job(redis_connection)
    _add_consumers_for_complete_job(redis_connection)
    _add_consumers_for_fail_job(redis_connection)
    _add_consumers_for_job_annotations(redis_connection)


_create_redis_instance_and_add_consumers()
