"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobDeployment(object):

    def __init__(self, job_id, job, job_source_bundle):
        from foundations_contrib.global_state import config_manager

        self._config = {}
        self._config.update(config_manager.config())
        self._config['_is_deployment'] = True

        self._job_id = job_id

    @staticmethod
    def scheduler_backend():
        raise NotImplementedError

    def config(self):
        return self._config

    def job_name(self):
        return self._job_id

    def deploy(self):
        pass

    def is_job_complete(self):
        pass

    def fetch_job_results(self):
        pass

    def get_job_status(self):
        pass

    def get_job_logs(self):
        pass
