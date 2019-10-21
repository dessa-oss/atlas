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
    def _get_internal(project_name, name):
        import os
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler

        scheduler_url = os.environ.get('FOUNDATIONS_SCHEDULER_URL', 'http://localhost:5000')
        scheduler = CronJobScheduler(scheduler_url)

        monitor_package = f'{project_name}-{name}'
        scheduled_job = scheduler.get_job(monitor_package)

        if scheduled_job is None:
            return None
        return scheduled_job
