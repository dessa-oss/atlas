"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SFTPJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from foundations.bucket_job_deployment import BucketJobDeployment
        from foundations_ssh.sftp_bucket import SFTPBucket

        self._deployment = BucketJobDeployment(
            job_name,
            job,
            job_source_bundle,
            SFTPBucket(self._code_path()),
            SFTPBucket(self._result_path())
        )

    @staticmethod
    def scheduler_backend():
        """Returns the default legacy scheduler backend implementation
        
        Returns:
            LegacyScheduler -- As above
        """

        from foundations_ssh.default_legacy_backend import DefaultLegacyBackend
        return DefaultLegacyBackend

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

    def get_job_status(self):
        import foundations.constants as constants
        if not self.is_job_complete():
            if self._is_job_queued():
                return constants.deployment_queued
            else:
                return constants.deployment_running
        else:
            results = self.fetch_job_results()

            try:
                error_information = results["global_stage_context"]["error_information"]

                if error_information is not None:
                    return constants.deployment_error
                else:
                    return constants.deployment_completed
            except:
                return constants.deployment_error

    def _code_path(self):
        from foundations.global_state import config_manager
        return config_manager['code_path']

    def _result_path(self):
        from foundations.global_state import config_manager
        return config_manager['result_path']

    def _is_job_queued(self):
        bucket = self._deployment._code_bucket
        job_name = self.job_name()
        return bucket.exists(job_name + ".tgz")