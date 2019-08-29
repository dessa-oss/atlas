"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobDeployment(object):

    def __init__(self, job_id, job, job_source_bundle):
        from foundations_contrib.job_bundler import JobBundler

        self._config = self._get_config()

        self._job_id = job_id
        self._job_bundler = JobBundler(self._job_id, self._config, job, job_source_bundle)
        #
        # self._scheduler = self._get_scheduler(self._config)

    @staticmethod
    def _get_config():
        from foundations_contrib.global_state import config_manager

        config = {}
        config.update(config_manager.config())
        config['_is_deployment'] = True

        return config
    #
    # @staticmethod
    # def _get_scheduler(config):
    #     from foundations_scheduler.scheduler import Scheduler
    #     from foundations_scheduler_core.kubernetes_api_wrapper import KubernetesApiWrapper
    #
    #     return Scheduler(KubernetesApiWrapper(), config)

    @staticmethod
    def scheduler_backend():
        raise NotImplementedError

    def config(self):
        return self._config

    def job_name(self):
        return self._job_id

    def deploy(self):
        from shutil import copy
        import tarfile
        from pathlib import Path
        import requests

        try:
            self._job_bundler.bundle()

            bundle_store_path = Path("/Users/el/working/temp/bundle_store/")
            archive_store_path = Path("/Users/el/working/temp/archive_store/")
            bundle_path = Path(self._job_bundler.job_archive())
            job_mount_path = archive_store_path / bundle_path.stem
            job_working_directory = archive_store_path / bundle_path.stem / "job_source"

            # put job bundle to job_bundle_path and job_archive
            copy(bundle_path, bundle_store_path)

            with tarfile.open(bundle_path) as tar:
                tar.extractall(path=archive_store_path)

            with tarfile.open(job_mount_path / "job.tgz") as tar:
                tar.extractall(path=job_working_directory)

            job_spec = self._create_job_spec(str(job_mount_path), self._job_id)

            print(job_spec)

            myurl = "http://127.0.0.1:5000/queued_jobs"
            r = requests.post(myurl, json=job_spec)
            print(r.status_code)
            print(r.json())

            #self._scheduler.submit_job(self._job_id, self._job_bundler.job_archive(), job_resources=self._job_resources(), worker_container_overrides=self._worker_container_override_config())
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self.get_job_status() == 'completed'

    def fetch_job_results(self):
        raise NotImplementedError

    def get_job_status(self):
        # from kubernetes.client.rest import ApiException
        #
        # try:
        #     return self._scheduler.get_job_status(self._job_id)
        # except ApiException as exception:
        #     if exception.status == 404:
        #         return None
        #     raise
        pass

    def get_job_logs(self):
        # return self._scheduler.get_job_logs(self._job_id)
        pass

    def stream_job_logs(self):
        # return self._scheduler.stream_job_logs(self._job_id)
        pass

    @staticmethod
    def cancel_jobs(jobs):
        # from foundations_scheduler.kubernetes_api_wrapper import KubernetesApiWrapper
        #
        # config = JobDeployment._get_config()
        # scheduler = JobDeployment._get_scheduler(config)
        #
        # api = KubernetesApiWrapper()
        # custom_objects_api = api.custom_objects_api()
        # batch_api = api.batch_api()
        #
        # return {job: JobDeployment._cancel_job(job, scheduler, custom_objects_api, batch_api) for job in jobs}
        pass

    @staticmethod
    def _cancel_job(job_id, scheduler, custom_objects_api, batch_api):
        pass
        # from kubernetes.client.rest import ApiException
        # from foundations_scheduler.kubernetes_api_wrapper import delete_options
        #
        # try:
        #     custom_objects_api.delete_namespaced_custom_object(
        #         'foundations.dessa.com',
        #         'v1',
        #         'foundations-scheduler-test',
        #         'foundations-jobs',
        #         job_id,
        #         delete_options()
        #     )
        #
        #     JobDeployment._try_to_delete_kubernetes_job(batch_api, job_id)
        #
        #     return True
        # except Exception as ex:
        #     return False

    def _worker_container_override_config(self):
        from foundations_contrib.global_state import config_manager

        return config_manager.config().get('worker_container_overrides', {})

    def _job_resources(self):
        from foundations_contrib.global_state import current_foundations_context
        return current_foundations_context().job_resources()
    #
    # @staticmethod
    # def _try_to_delete_kubernetes_job(batch_api, job_id):
    #     import time
    #     from kubernetes.client.rest import ApiException
    #     from foundations_scheduler.kubernetes_api_wrapper import delete_options
    #
    #     latest_exception = None
    #
    #     for _ in range(5):
    #         try:
    #             batch_api.delete_namespaced_job(
    #                 'foundations-job-{}'.format(job_id),
    #                 'foundations-scheduler-test',
    #                 delete_options()
    #             )
    #
    #             return
    #         except ApiException as ex:
    #             latest_exception = ex
    #             time.sleep(0.5)
    #             continue
    #
    #     raise latest_exception

    def _create_job_spec(self, job_mount_path, job_id):
        return \
{

    "image": "python:3.6-alpine",
    "volumes":
    {
        job_mount_path:
        {
            "bind": "/job",
            "mode": "rw"
        }
    },
    "working_dir": "/job/job_source",
    "environment":
    {
        "JOB_ID": job_id,
        "ENTRYPOINT": "test.py",
        "PYTHONPATH": "/job"
    },
    "entrypoint": ["/bin/sh", "-c"],
    "command": ["python ${ENTRYPOINT}"]
}