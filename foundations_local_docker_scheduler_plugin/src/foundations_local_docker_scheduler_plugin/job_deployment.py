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
        self._job = job

    @staticmethod
    def _get_config():
        from foundations_contrib.global_state import config_manager

        config = {}
        config.update(config_manager.config())
        config['_is_deployment'] = True

        return config

    @staticmethod
    def scheduler_backend():
        raise NotImplementedError

    def config(self):
        return self._config

    def job_name(self):
        return self._job_id

    def deploy(self):
        import tarfile
        from pathlib import Path
        import requests

        try:
            self._job_bundler.bundle()

            #TODO feature request on local docker scheduler to support copying instead of mounting the working dir
            working_dir_root_path = Path(self._config['working_dir_root'])
            bundle_path = Path(self._job_bundler.job_archive())
            job_mount_path = working_dir_root_path / bundle_path.stem
            job_working_dir_path = working_dir_root_path / bundle_path.stem / "job_source"

            # # If we need to capture and persist the starting state of the job bundle
            # # put job bundle to job_bundle_path
            # job_store_root_path = Path(config['job_store_root'])
            # from shutil import copy
            # copy(bundle_path, job_store_root_path)

            with tarfile.open(bundle_path) as tar:
                tar.extractall(path=working_dir_root_path)

            with tarfile.open(job_mount_path / "job.tgz") as tar:
                tar.extractall(path=job_working_dir_path)

            project_name = self._job.pipeline_context().provenance.project_name
            username = self._job.pipeline_context().provenance.user_name

            job_spec = self._create_job_spec(job_mount_path=str(job_mount_path.absolute()),
                                             working_dir_root_path=str(working_dir_root_path.absolute()),
                                             job_results_root_path=self._config['job_results_root'],
                                             container_config_root_path=self._config['container_config_root'],
                                             job_id=self._job_id,
                                             project_name=project_name,
                                             username=username,
                                             worker_container_overrides=self._config['worker_container_overrides'])

            myurl = f"{self._config['scheduler_url']}/queued_jobs"
            r = requests.post(myurl, json={'job_id': self._job_id,
                                           'spec': job_spec,
                                           'metadata': {'project_name': project_name,
                                                        'username': username}
                                           })
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self.get_job_status() == 'completed'

    def fetch_job_results(self):
        raise NotImplementedError

    def get_job_status(self):
        import requests

        responses = {
            "queued": "queued",
            "running": "running",
            "failed": "completed",
            "completed": "completed",
            "pending": "queued"
        }

        r = requests.get(f"{self._config['scheduler_url']}/jobs/{self._job_id}")
        if r.status_code == requests.codes.ok:
            return responses[r.json()['status']]
        else:
            return None

    def get_job_logs(self):
        import requests

        r = requests.get(f"{self._config['scheduler_url']}/jobs/{self._job_id}")
        if r.status_code == requests.codes.ok:
            return r.json()['logs']
        else:
            return ""

    def stream_job_logs(self, strip_new_line=True):
        import requests
        import time

        status = self.get_job_status()

        while status == "queued" or status is None:
            time.sleep(1)
            status = self.get_job_status()

        if status == "running":
            r = requests.get(f"{self._config['scheduler_url']}/running_jobs/{self._job_id}/container_id")
            if r.status_code == requests.codes.ok:
                import docker
                client = docker.from_env()

                container = client.containers.get(r.json())

                log_stream = container.logs(stream=True)

                for line in log_stream:
                    if strip_new_line:
                        line = line.decode().strip('\n')
                    else:
                        line = line.decode()
                    yield line
            else:
                # try and see if it completed in between requests
                status = "completed"

        if status == "completed":
            from io import StringIO
            log_stream = StringIO(self.get_job_logs())

            for line in log_stream:
                if strip_new_line:
                    line = line.strip('\n')
                yield line


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

    def _job_resources(self):
        from foundations_contrib.global_state import current_foundations_context
        return current_foundations_context().job_resources()

    def _create_job_spec(self, job_mount_path, working_dir_root_path, job_results_root_path, container_config_root_path, job_id, project_name, username, worker_container_overrides):
        from foundations_contrib.global_state import current_foundations_context
        worker_container = {
            'image': "atlas-ce/worker:latest",
            'volumes':
                {
                    job_mount_path:
                        {
                            "bind": "/job",
                            "mode": "rw"
                        },
                    job_results_root_path:
                        {
                            "bind": job_results_root_path,
                            "mode": "rw"
                        },
                    container_config_root_path:
                        {
                            "bind": "/root/.foundations/config",
                            "mode": "rw"
                        },
                    working_dir_root_path:
                        {
                            "bind": working_dir_root_path,
                            "mode": "rw"
                        }
                },
             "working_dir": "/job/job_source",
                # [
                # {
                #     'name': 'logging',
                #     'mountPath': '/root/.foundations/logs',
                # },
                # {
                #     'name': 'execution-config',
                #     'mountPath': '/root/.foundations/config/execution'
                # }
                # ]
            'environment':
                {
                    "FOUNDATIONS_USER": username,
                    "FOUNDATIONS_JOB_ID": job_id,
                    "FOUNDATIONS_PROJECT_NAME": project_name,
                    "PYTHONPATH": "/job/",
                    "FOUNDATIONS_HOME": "/root/.foundations/"
                },
            "network": "foundations-atlas"
        }

        if current_foundations_context().job_resources().ram is not None:
            worker_container['mem_limit'] = int(current_foundations_context().job_resources().ram)

        if (current_foundations_context().job_resources().num_gpus is not None
                and current_foundations_context().job_resources().num_gpus > 0):
            worker_container['runtime'] = 'nvidia'
        else:
            worker_container['runtime'] = 'runc'

        for override_key in ['command', 'image', 'workingDir', 'imagePullPolicy']:
            if override_key in worker_container_overrides:
                worker_container[override_key] = worker_container_overrides[override_key]

        if 'args' in worker_container_overrides:
            worker_container['command'] = worker_container_overrides['args']
        #
        # if not has_gpus:
        #     worker_container['env'] += [{'name': 'NVIDIA_VISIBLE_DEVICES', 'value': ''}]

        for override_key in ['environment', 'volumes']:
            if override_key in worker_container_overrides:
                worker_container[override_key] = {**worker_container[override_key], **worker_container_overrides[override_key]}

        if 'resources' in worker_container_overrides:
            for override_key in ['limits', 'requests']:
                if override_key in worker_container_overrides['resources']:
                    worker_container['resources'][override_key].update(
                        worker_container_overrides['resources'][override_key])

        return worker_container