

def _expect_code(status_code):
    def _decorator(method):
        def _wrapped_method(*args, **kwargs):
            response = method(*args, **kwargs)
            if response.status_code != status_code:
                raise CronJobSchedulerError(response.text)
            return response
        return _wrapped_method
    return _decorator


class CronJobScheduler(object):
    def __init__(self, scheduler_url=None):
        import requests
        from foundations_authentication.user_token import user_token

        if scheduler_url is None:
            scheduler_url = "http://localhost:5000"

        self._scheduler_uri = scheduler_url
        self._raw_api = requests
        self._user_token = user_token

    def pause_job(self, job_id):
        self._change_job_status(job_id, "paused")

    def resume_job(self, job_id):
        self._change_job_status(job_id, "active")

    @_expect_code(201)
    def schedule_job(self, job_id, spec, schedule, metadata=None, gpu_spec=None):
        return self._raw_api.post(
            self._jobs_uri(),
            json={
                "job_id": job_id,
                "spec": spec,
                "gpu_spec": gpu_spec,
                "metadata": metadata,
                "schedule": schedule,
            },
            headers={"Authorization": f"Bearer {self._user_token()}"},
        )

    def get_jobs(self):
        return self._get_jobs().json()

    def get_job(self, job_id):
        return self._get_job(job_id).json()

    def get_job_with_params(self, params):
        return self._get_jobs(params).json()

    @_expect_code(204)
    def update_job_schedule(self, job_id, schedule):
        return self._raw_api.patch(
            self._job_uri(job_id),
            json={"schedule": schedule},
            headers={"Authorization": f"Bearer {self._user_token()}"},
        )

    @_expect_code(204)
    def delete_job(self, job_id):
        return self._raw_api.delete(
            self._job_uri(job_id),
            headers={"Authorization": f"Bearer {self._user_token()}"},
        )

    @_expect_code(204)
    def _change_job_status(self, job_id, status):
        return self._raw_api.put(
            self._job_uri(job_id),
            json={"status": status},
            headers={"Authorization": f"Bearer {self._user_token()}"},
        )

    @_expect_code(200)
    def _get_job(self, job_id):
        return self._raw_api.get(
            self._job_uri(job_id),
            headers={"Authorization": f"Bearer {self._user_token()}"},
        )

    @_expect_code(200)
    def _get_jobs(self, params=None):
        if params:
            return self._raw_api.get(
                self._jobs_uri(),
                params=params,
                headers={"Authorization": f"Bearer {self._user_token()}"},
            )
        return self._raw_api.get(
            self._jobs_uri(), headers={"Authorization": f"Bearer {self._user_token()}"}
        )

    def _jobs_uri(self):
        return f"{self._scheduler_uri}/scheduled_jobs"

    def _job_uri(self, job_id):
        return f"{self._jobs_uri()}/{job_id}"


class CronJobSchedulerError(Exception):
    pass
