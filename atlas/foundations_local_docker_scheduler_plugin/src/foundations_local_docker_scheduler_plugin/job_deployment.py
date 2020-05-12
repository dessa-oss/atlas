
from foundations_authentication.user_token import user_token


class JobDeployment(object):
    def __init__(self, job_id, job, job_source_bundle):

        self._config = self._get_config()

        self._job_id = job_id
        self._job_bundler = None
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

    def _is_local_deployment(self):
        return '127.0.0.1' in self._config['scheduler_url'] or 'localhost' in self._config['scheduler_url']

    def _get_paths(self):
        from pathlib import Path, PurePosixPath
        from sys import platform
        working_dir_root_path = Path(self._config['working_dir_root'])
        bundle_path = Path(self._job_bundler.job_archive())
        job_mount_path = working_dir_root_path / bundle_path.stem

        if platform == 'win32':
            if self._is_local_deployment():
                working_dir_root_path = convert_win_path_to_posix(working_dir_root_path)
                job_mount_path = convert_win_path_to_posix(job_mount_path)
                job_results_root_path = convert_win_path_to_posix(Path(self._config['job_results_root']))
                container_config_root_path = convert_win_path_to_posix(Path(self._config['container_config_root']))
            else:
                working_dir_root_path = PurePosixPath(self._config['working_dir_root'])
                bundle_path = PurePosixPath(self._job_bundler.job_archive())
                job_mount_path = working_dir_root_path / bundle_path.stem
                job_mount_path = str(job_mount_path)
                working_dir_root_path = str(working_dir_root_path)
                job_results_root_path = self._config['job_results_root']
                container_config_root_path = self._config['container_config_root']
        else:
            job_mount_path = str(job_mount_path.absolute())
            working_dir_root_path = str(working_dir_root_path.absolute())
            job_results_root_path = self._config['job_results_root']
            container_config_root_path = self._config['container_config_root']

        return job_mount_path, working_dir_root_path, job_results_root_path, container_config_root_path

    def deploy(self):
        import requests
        from foundations_local_docker_scheduler_plugin.bundle_deployment import job_bundle, submit_job_bundle

        try:
            self._job_bundler = job_bundle(self._job_id)
            response = submit_job_bundle(self._job_bundler)

            if response.status_code != 200:
                 raise RuntimeError(f'Unable to submit job bundle. {response.text}')

            project_name = self._job.project_name
            username = self._job.user_name

            job_mount_path, working_dir_root_path, job_results_root_path, container_config_root_path = self._get_paths()

            job_spec = self._create_job_spec(job_mount_path=job_mount_path,
                                             working_dir_root_path=working_dir_root_path,
                                             job_results_root_path=job_results_root_path,
                                             container_config_root_path=container_config_root_path,
                                             job_id=self._job_id,
                                             project_name=project_name,
                                             username=username,
                                             worker_container_overrides=self._config['worker_container_overrides'])

            gpu_spec = self._create_gpu_spec()

            queue_job_url = f"{self._config['scheduler_url']}/queued_jobs"
            payload = {
                'job_id': self._job_id,
                'spec': job_spec,
                'metadata': {
                    'project_name': project_name,
                    'username': username
                },
                'gpu_spec': gpu_spec
            }

            response = requests.post(queue_job_url, json=payload, headers={"Authorization": f"bearer {user_token()}"})
            if response.status_code != 201:
                 raise RuntimeError(f'Unable to add job to the queue. {response.text}')

        except requests.exceptions.ConnectionError as e:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self.get_job_status() == 'completed'

    def fetch_job_results(self):
        raise NotImplementedError

    def get_job_status(self):
        return self._get_job_status(self._job_id)

    def _get_job_status(self, job_id):
        import requests

        responses = {
            "queued": "queued",
            "running": "running",
            "failed": "completed",
            "completed": "completed",
            "pending": "queued"
        }
        try:
            r = requests.get(f"{self._config['scheduler_url']}/jobs/{job_id}", headers={"Authorization": f"bearer {user_token()}"})
            if r.status_code == requests.codes.ok:
                return responses[r.json()['status']]
            else:
                return None
        except:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')

    def get_true_job_status(self):
        import requests

        try:
            r = requests.get(f"{self._config['scheduler_url']}/jobs/{self._job_id}", headers={"Authorization": f"bearer {user_token()}"})
            if r.status_code == requests.codes.ok:
                return r.json()['status']
            else:
                return None
        except:
            raise ConnectionError('Cannot currently find Atlas server. Start Atlas server with `atlas-server start`.')

    def get_job_logs(self):
        import requests

        r = requests.get(f"{self._config['scheduler_url']}/jobs/{self._job_id}", headers={"Authorization": f"bearer {user_token()}"})
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
            r = requests.get(f"{self._config['scheduler_url']}/running_jobs/{self._job_id}/container_id", headers={"Authorization": f"bearer {user_token()}"})
            if r.status_code == requests.codes.ok:
                import docker
                from docker.errors import APIError
                from requests.exceptions import ConnectionError

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
                    from foundations_contrib.global_state import log_manager
                    logger = log_manager.get_logger(__name__)
                    logger.warn(f"Could not find local container for job {self._job_id}. The job may have already completed or was submitted to a remote machine. Please see the GUI for full job logs and status.")

                except ConnectionError as e:
                    from foundations_contrib.global_state import log_manager
                    logger = log_manager.get_logger(__name__)
                    logger.warn(f"Could not connect to local Docker engine for job {self._job_id}. You can ignore this warning if the job was submitted to a remote machine. Please see the GUI for full job logs and status.")


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
        scheduler_url = config_manager['scheduler_url']

        return {job: JobDeployment._cancel_job(job, scheduler_url) for job in jobs}


    @staticmethod
    def _cancel_job(job_id, scheduler_url):
        import os
        import requests

        try:
            requests.delete(f"{scheduler_url}/completed_jobs/{job_id}", headers={"Authorization": f"bearer {user_token()}"}).raise_for_status()
            return True

        except Exception as ex:
            return False

    def _job_resources(self):
        from foundations_contrib.global_state import current_foundations_context
        return current_foundations_context().job_resources

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
                    "FOUNDATIONS_HOME": "/root/.foundations/",
                    "FOUNDATIONS_TOKEN": user_token()
                },
            "network": "foundations-atlas"
        }

        if current_foundations_context().job_resources.ram is not None:
            worker_container['mem_limit'] = int(current_foundations_context().job_resources.ram)

        if (current_foundations_context().job_resources.num_gpus is not None
                and current_foundations_context().job_resources.num_gpus > 0):
            worker_container['image'] = 'us.gcr.io/dessa-atlas/worker-gpu:latest'
            worker_container['runtime'] = 'nvidia'

        else:
            worker_container['image'] = 'us.gcr.io/dessa-atlas/worker:latest'
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

    def _create_gpu_spec(self):
        from foundations_contrib.global_state import foundations_context
        resources = foundations_context.job_resources
        gpu_spec = {
            "num_gpus": resources.num_gpus
        }
        return gpu_spec

    def stop_running_job(self):
        import requests

        r = requests.delete(f"{self._config['scheduler_url']}/running_jobs/{self._job_id}", headers={"Authorization": f"bearer {user_token()}"})
        return 200 <= r.status_code < 300

    def get_job_archive(self):
        import requests
        import os

        res = requests.get(f"{self._config['scheduler_url']}/job_bundle/{self._job_id}", headers={"Authorization": f"bearer {user_token()}"})

        if res.status_code in [401, 404]:
            return False
        else:
            with open(f"{os.getcwd()}/{self._job_id}.tgz", "wb") as file:
                file.write(res.content)
            return True

    @staticmethod
    def clear_queue():
        import requests

        config = JobDeployment._get_config()

        num_removed = 0
        status_code = requests.delete(f"{config['scheduler_url']}/queued_jobs/0", headers={"Authorization": f"bearer {user_token()}"}).status_code

        while status_code == 204:
            status_code = requests.delete(f"{config['scheduler_url']}/queued_jobs/0", headers={"Authorization": f"bearer {user_token()}"}).status_code
            num_removed += 1

        return num_removed

def convert_win_path_to_posix(win_path):
    win_path_full = str(win_path.absolute().as_posix()).split(':')
    win_drive = '/' + win_path_full[0].lower()
    win_path = win_path_full[1]
    posix_path = ''.join((win_drive, win_path))
    return posix_path
