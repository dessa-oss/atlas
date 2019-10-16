"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CronJobScheduler(object):

    def __init__(self, host=None, port=None):
        import importlib
        
        if host is None:
            host = 'localhost'
        
        if port is None:
            port = 5000

        self._scheduler_uri = f'http://{host}:{port}'
        self._raw_api = importlib.import_module('requests')

    def pause_job(self, job_id):
        self._raw_api.put(f'{self._scheduler_uri}/scheduled_jobs/{job_id}', json={'status': 'paused'})

    def resume_job(self, job_id):
        pass

    def schedule_job(self, job_id, spec, schedule, job_bundle_path, metadata=None, gpu_spec=None):
        pass

    def get_scheduled_jobs(self):
        pass

    def get_scheduled_job(self, job_id):
        pass

    def update_job_schedule(self, job_id):
        pass

    def delete_job(self, job_id):
        pass