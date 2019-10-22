"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ScheduledMonitor(object):

    @staticmethod
    def get(project_name=None, name=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ScheduledMonitor._get_internal(project_name, name))

    @staticmethod
    def delete(project_name=None, name=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ScheduledMonitor._delete_internal(project_name, name))

    @staticmethod
    def patch(project_name=None, name=None, schedule=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ScheduledMonitor._patch_internal(project_name, name, schedule))


    @staticmethod
    def _scheduler():
        import os
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler

        scheduler_url = os.environ.get('FOUNDATIONS_SCHEDULER_URL', 'http://localhost:5000')
        return CronJobScheduler(scheduler_url)

    @staticmethod
    def _get_internal(project_name, name):
        monitor_package = f'{project_name}-{name}'
        scheduled_job = ScheduledMonitor._scheduler().get_job(monitor_package)

        if scheduled_job is None:
            return None
        return scheduled_job

    @staticmethod
    def _delete_internal(project_name, name):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError

        monitor_package = f'{project_name}-{name}'
        try:
            response = ScheduledMonitor._scheduler().delete_job(monitor_package)
            return {}
        except CronJobSchedulerError as ex:
            return None

    @staticmethod
    def _patch_internal(project_name, name, schedule):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError

        monitor_package = f'{project_name}-{name}'

        try:
            response = ScheduledMonitor._scheduler().update_job_schedule(monitor_package, schedule)
            return {}
        except CronJobSchedulerError as ex:
            return None

