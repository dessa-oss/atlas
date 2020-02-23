

class ScheduledMonitorsListing(object):

    @staticmethod
    def get(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ScheduledMonitorsListing._get_internal(project_name))

    @staticmethod
    def _get_internal(project_name):
        import os
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler

        scheduler_url = os.environ.get('FOUNDATIONS_SCHEDULER_URL', 'http://localhost:5000')
        scheduler = CronJobScheduler(scheduler_url)

        params = {'project': project_name}
        project_monitors = scheduler.get_job_with_params(params)

        if project_monitors is None:
            return None
        return project_monitors