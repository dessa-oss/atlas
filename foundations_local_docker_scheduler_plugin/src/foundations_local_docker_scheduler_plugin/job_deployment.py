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
        from sys import platform
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

            if platform == 'win32':
                working_dir_root_path = convert_win_path_to_posix(working_dir_root_path)
                job_mount_path = convert_win_path_to_posix(job_mount_path)
                job_results_root_path = convert_win_path_to_posix(Path(self._config['job_results_root']))
                container_config_root_path = convert_win_path_to_posix(Path(self._config['container_config_root']))

            else:
                job_mount_path = str(job_mount_path.absolute())
                working_dir_root_path = str(working_dir_root_path.absolute())
                job_results_root_path = self._config['job_results_root']
                container_config_root_path = self._config['container_config_root']

            job_spec = self._create_job_spec(job_mount_path=job_mount_path,
                                             working_dir_root_path=working_dir_root_path,
                                             job_results_root_path=job_results_root_path,
                                             container_config_root_path=container_config_root_path,
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
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self.get_job_status() == 'completed'

    def fetch_job_results(self):
        raise NotImplementedError

    def get_job_status(self):
        return self._get_job_status(self._job_id)

    @staticmethod
    def _get_job_status(job_id):
        import requests
        from foundations_contrib.global_state import config_manager

        responses = {
            "queued": "queued",
            "running": "running",
            "failed": "completed",
            "completed": "completed",
            "pending": "queued"
        }
        try:
            r = requests.get(f"{config_manager['scheduler_url']}/jobs/{job_id}")
            if r.status_code == requests.codes.ok:
                return responses[r.json()['status']]
            else:
                return None
        except:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')

    def get_true_job_status(self):
        import requests

        try:
            r = requests.get(f"{self._config['scheduler_url']}/jobs/{self._job_id}")
            if r.status_code == requests.codes.ok:
                return r.json()['status']
            else:
                return None
        except:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')

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
        counter = 0
        timeout = 15

        while status == "queued" or status is None:
            time.sleep(1)
            if status is None:
                counter += 1
            if counter >= timeout:
                raise TimeoutError('Job timed out')
            status = self.get_job_status()

        if status == "running":
            r = requests.get(f"{self._config['scheduler_url']}/running_jobs/{self._job_id}/container_id")
            if r.status_code == requests.codes.ok:
                import docker
                from docker.errors import APIError

                try:
                    client = docker.from_env()
                    container = client.containers.get(r.json())
                    log_stream = container.logs(stream=True)

                    for line in log_stream:
                        if strip_new_line:
                            line = line.decode().strip('\n')
                        else:
                            line = line.decode()
                        yield line

                except APIError as e:
                    APIError(f"Could not find container for job {self._job_id}. Job may have completed. ")
                    status = "completed"

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
        from foundations_contrib.global_state import config_manager
        from pathlib import Path
        archive_path = str(Path(config_manager['job_results_root']) / 'archive')
        scheduler_url = config_manager['scheduler_url']

        return {job: JobDeployment._cancel_job(job, scheduler_url, archive_path) for job in jobs}


    @staticmethod
    def _cancel_job(job_id, scheduler_url, archive_path):
        import os
        import requests

        try:
            requests.delete(f"{scheduler_url}/completed_jobs/{job_id}").raise_for_status()
            return True

        except Exception:
            return False

    def _job_resources(self):
        from foundations_contrib.global_state import current_foundations_context
        return current_foundations_context().job_resources()

    def _create_job_spec(self, job_mount_path, working_dir_root_path, job_results_root_path, container_config_root_path, job_id, project_name, username, worker_container_overrides):
        from foundations_contrib.global_state import current_foundations_context

        worker_container = {

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
            worker_container['image'] = 'us.gcr.io/atlas-ce/worker-gpu:latest'
            worker_container['runtime'] = 'nvidia'

        else:
            worker_container['image'] = 'us.gcr.io/atlas-ce/worker:latest'
            worker_container['runtime'] = 'runc'

        for override_key in ['command', 'image', 'working_dir', 'entrypoint']:
            if override_key in worker_container_overrides:
                worker_container[override_key] = worker_container_overrides[override_key]
        if self._config['run_script_environment']['script_to_run']:
            worker_container['entrypoint'] = self._config['run_script_environment']['script_to_run']

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

    def stop_running_job(self):
        import requests

        r = requests.delete(f"{self._config['scheduler_url']}/running_jobs/{self._job_id}")
        return 200 <= r.status_code < 300

    @staticmethod
    def clear_queue():
        import requests

        config = JobDeployment._get_config()

        num_removed = 0
        status_code = requests.delete(f"{config['scheduler_url']}/queued_jobs/0").status_code

        while status_code == 204:
            status_code = requests.delete(f"{config['scheduler_url']}/queued_jobs/0").status_code
            num_removed += 1

        return num_removed

def convert_win_path_to_posix(win_path):
    win_path_full = str(win_path.absolute().as_posix()).split(':')
    win_drive = '/' + win_path_full[0].lower()
    win_path = win_path_full[1]
    posix_path = ''.join((win_drive, win_path))
    return posix_path
