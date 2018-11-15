"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.global_state import message_router

_add_listener = message_router.add_listener


def _add_consumers_for_stage_log_middleware(redis):
    from foundations.consumers.job_metric_consumer import JobMetricConsumer
    from foundations.consumers.job_metric_name_consumer import JobMetricNameConsumer

    _add_listener(JobMetricConsumer(redis), 'job_metrics')
    _add_listener(JobMetricNameConsumer(redis), 'job_metrics')


def _add_consumers_for_queue_job(redis):
    from foundations.consumers.jobs.queued.creation_time import CreationTime
    from foundations.consumers.jobs.queued.input_parameter_keys import InputParameterKeys
    from foundations.consumers.jobs.queued.input_parameters import InputParameters
    from foundations.consumers.jobs.queued.job_state import JobState
    from foundations.consumers.jobs.queued.project_listing import ProjectListing
    from foundations.consumers.jobs.queued.project_name import ProjectName
    from foundations.consumers.jobs.queued.run_data_keys import RunDataKeys
    from foundations.consumers.jobs.queued.run_data import RunData

    import json

    _add_listener(CreationTime(redis), 'queue_job')
    _add_listener(InputParameterKeys(redis), 'queue_job')
    _add_listener(InputParameters(redis, json), 'queue_job')
    _add_listener(JobState(redis), 'queue_job')
    _add_listener(ProjectListing(redis), 'queue_job')
    _add_listener(ProjectName(redis), 'queue_job')
    _add_listener(RunDataKeys(redis), 'queue_job')
    _add_listener(RunData(redis, json), 'queue_job')


def _add_consumers_for_run_job(redis):
    from foundations.consumers.jobs.running.job_state import JobState
    from foundations.consumers.jobs.running.project_listing import ProjectListing
    from foundations.consumers.jobs.running.remove_queued_job import RemoveQueuedJob
    from foundations.consumers.jobs.running.start_time import StartTime

    _add_listener(JobState(redis), 'run_job')
    _add_listener(ProjectListing(redis), 'run_job')
    _add_listener(RemoveQueuedJob(redis), 'run_job')
    _add_listener(StartTime(redis), 'run_job')


def _add_consumers_for_complete_job(redis):
    from foundations.consumers.jobs.completed.completed_time import CompletedTime
    from foundations.consumers.jobs.completed.job_state import JobState

    _add_listener(CompletedTime(redis), 'complete_job')
    _add_listener(JobState(redis), 'complete_job')


def _add_consumers_for_fail_job(redis):
    from foundations.consumers.jobs.completed.completed_time import CompletedTime
    from foundations.consumers.jobs.failed.error_data import ErrorData
    from foundations.consumers.jobs.failed.job_state import JobState

    _add_listener(CompletedTime(redis), 'fail_job')
    _add_listener(CompletedTime(redis), 'fail_job')
    _add_listener(JobState(redis), 'fail_job')


def _create_redis_instance_and_add_consumers():
    import redis
    from foundations.helpers.lazy_redis import LazyRedis

    redis = LazyRedis(redis.Redis)
    _add_consumers_for_stage_log_middleware(redis)
    _add_consumers_for_queue_job(redis)
    _add_consumers_for_run_job(redis)
    _add_consumers_for_complete_job(redis)
    _add_consumers_for_fail_job(redis)


_create_redis_instance_and_add_consumers()
