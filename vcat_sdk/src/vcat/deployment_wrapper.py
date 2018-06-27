"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DeploymentWrapper(object):
    def __init__(self, deployment):
        self._deployment = deployment

    def job_name(self):
        return self._deployment.job_name()

    def is_job_complete(self):
        return self._deployment.is_job_complete()

    def fetch_job_results(self, wait_seconds=5, verbose_errors=False):
        from vcat.remote_exception import check_result
        
        if not self.is_job_complete():
            self.wait_for_deployment_to_complete(wait_seconds=wait_seconds)

        result = self._deployment.fetch_job_results()
        return check_result(self.job_name(), result, verbose_errors)

    def wait_for_deployment_to_complete(self, wait_seconds=5):
        import time
        from vcat.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self.is_job_complete():
            log.info("waiting for job `" + self.job_name() + "` to finish")
            time.sleep(wait_seconds)

        log.info("job `" + self.job_name() + "` completed")