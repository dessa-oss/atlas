"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobDeployment(object):

    def __init__(self, job_id, job, job_source_bundle):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.job_bundler import JobBundler
        from foundations_scheduler.scheduler import Scheduler
        from foundations_scheduler_core.kubernetes_api_wrapper import KubernetesApiWrapper

        self._config = {}
        self._config.update(config_manager.config())
        self._config['_is_deployment'] = True

        self._job_id = job_id
        self._job_bundler = JobBundler(self._job_id, self._config, job, job_source_bundle)

        self._scheduler = Scheduler(KubernetesApiWrapper(), self._config)

    @staticmethod
    def scheduler_backend():
        raise NotImplementedError

    def config(self):
        return self._config

    def job_name(self):
        return self._job_id

    def deploy(self):
        try:
            self._job_bundler.bundle()
            self._scheduler.submit_job(self._job_id, self._job_bundler.job_archive(), job_resources=self._job_resources())
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self.get_job_status() == 'completed'

    def fetch_job_results(self):
        raise NotImplementedError

    def get_job_status(self):
        return self._scheduler.get_job_status(self._job_id)

    def get_job_logs(self):
        return self._scheduler.get_job_logs(self._job_id)

    @staticmethod
    def cancel_jobs(jobs):
        from foundations_scheduler.kubernetes_api_wrapper import KubernetesApiWrapper

        api = KubernetesApiWrapper()
        custom_objects_api = api.custom_objects_api()
        batch_api = api.batch_api()

        return {job: JobDeployment._cancel_job(job, custom_objects_api, batch_api) for job in jobs}

    @staticmethod
    def _cancel_job(job_id, custom_objects_api, batch_api):
        from kubernetes.client.rest import ApiException
        from foundations_scheduler.kubernetes_api_wrapper import delete_options

        try:
            custom_objects_api.delete_namespaced_custom_object(
                'foundations.dessa.com',
                'v1',
                'foundations-scheduler-test',
                'foundations-jobs',
                job_id,
                delete_options()
            )

            batch_api.delete_namespaced_job(
                'foundations-job-{}'.format(job_id),
                'foundations-scheduler-test',
                delete_options()
            )

            return True
        except:
            return False

    def _job_resources(self):
        from foundations_contrib.global_state import current_foundations_context
        return current_foundations_context().job_resources()