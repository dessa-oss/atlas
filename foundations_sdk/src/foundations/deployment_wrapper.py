"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DeploymentWrapper(object):
    """
    Provides user-facing functionality to deployment classes created through integrations (e.g. LocalShellJobDeployment, GCPJobDeployment)

    Arguments:
        deployment: {*JobDeployment} -- The integration-level job deployment to wrap
    """

    def __init__(self, deployment):
        self._deployment = deployment

    def job_name(self):
        """
        Gets the name of the job being run

        Arguments:
            - This method doesn't receive arguments.

        Returns:
            job_name {string} -- The name of the job being run

        Raises:
            - This method normally doesn't raise any exception.
        """

        return self._deployment.job_name()

    def is_job_complete(self):
        """
        Returns whether the job being run has completed

        Arguments:
            - This method doesn't receive arguments.

        Returns:
            is_job_complete {boolean} -- True if the job is done, False otherwise (regardless of success / failure)

        Raises:
            - This method normally doesn't raise any exception.
        """

        return self._deployment.is_job_complete()

    def fetch_job_results(self, wait_seconds=5):
        """
        Waits for the job to complete and then fetches the results for the job

        Arguments:
            wait_seconds {float} -- The number of seconds to wait between job status check attempts (defaults to 5)
            verbose_errors {bool} -- Whether to output stack trace entries relating to Foundations in the event of an exception (defaults to False)

        Returns:
            results_dict {dictionary} -- Dict representing a more-or-less "serialized" PipelineContext for the job.  Will raise a RemoteException in the event of an exception thrown in the execution environment

        Raises:
            - This method normally doesn't raise any exception.
        """

        from foundations_internal.remote_exception import check_result

        if not self.is_job_complete():
            self.wait_for_deployment_to_complete(wait_seconds=wait_seconds)

        result = self._deployment.fetch_job_results()
        return check_result(self.job_name(), result)

    def wait_for_deployment_to_complete(self, wait_seconds=5):
        """
        Waits for the job to complete

        Arguments:
            wait_seconds {float} -- The number of seconds to wait between job status check attempts (defaults to 5)

        Returns:
            - This method doesn't return a value.

        Raises:
            - This method normally doesn't raise any exception.
        """

        import time
        from foundations.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self.is_job_complete():
            log.info("waiting for job `" + self.job_name() + "` to finish")
            time.sleep(wait_seconds)

        log.info("job `" + self.job_name() + "` completed")

    def get_job_status(self):
        """
        Similar to is_job_complete, but with more information

        Arguments:
            - This method doesn't receive arguments.

        Returns:
            status {string} -- String, which is either "Queued", "Running", "Completed", or "Error"

        Raises:
            - This method normally doesn't raise any exception.
        """

        return self._deployment.get_job_status()

    def _try_get_results(self, error_handler):
        from foundations.deployment_utils import extract_results

        try:
            return extract_results(self.fetch_job_results())
        except Exception as e:
            if error_handler is not None:
                error_handler(e)
            else:
                raise e
