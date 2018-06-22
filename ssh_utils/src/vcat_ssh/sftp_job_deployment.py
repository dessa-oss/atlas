"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SFTPJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from vcat.bucket_job_deployment import BucketJobDeployment
        from vcat_ssh.sftp_bucket import SFTPBucket

        self._deployment = BucketJobDeployment(
            job_name,
            job,
            job_source_bundle,
            SFTPBucket(self._code_path()),
            SFTPBucket(self._result_path())
        )

    def config(self):
        return self._deployment.config()

    def job_name(self):
        return self._deployment.job_name()

    def deploy(self):
        return self._deployment.deploy()

    def is_job_complete(self):
        return self._deployment.is_job_complete()

    def fetch_job_results(self):
        return self._deployment.fetch_job_results()

    def _code_path(self):
        from vcat.global_state import config_manager
        return config_manager['code_path']

    def _result_path(self):
        from vcat.global_state import config_manager
        return config_manager['result_path']
