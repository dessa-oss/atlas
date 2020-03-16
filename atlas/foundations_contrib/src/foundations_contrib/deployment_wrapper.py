class DeploymentWrapper(object):
    """
    ### The three numerals at the begining are a marker for not generating user documentation for the class.
    Provides user-facing functionality to deployment classes created through integrations (e.g. LocalShellJobDeployment, GCPJobDeployment)

    Arguments:
        deployment: {*JobDeployment} -- The integration-level job deployment to wrap
    """

    def __init__(self, deployment):
        self._deployment = deployment

    def job_name(self):
        return self._deployment.job_name()

    def is_job_complete(self):
        """
        Returns whether the job being run has completed

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            is_job_complete {boolean} -- True if the job is done, False otherwise (regardless of success / failure)

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.is_job_complete()

    def get_job_details(self, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        formatted_job_data = JobDataRedis(pipe, self.job_name()).get_formatted_job_data()
        return formatted_job_data

    def get_metric(self, metric_name, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        metric = JobDataRedis(pipe, self.job_name()).get_job_metric(metric_name)
        return metric

    def get_param(self, param_name, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        param = JobDataRedis(pipe, self.job_name()).get_job_param(param_name)
        return param

    def wait_for_deployment_to_complete(self, wait_seconds=5, log_output=True):
        """
        Waits for the job to complete. It checks the status of the job periodically to test for completion.

        Arguments:
            wait_seconds {float} -- The number of seconds to wait between job status check attempts (defaults to 5)

        Returns:
            - This method doesn't return a value.

        Raises:
            - This method doesn't raise any exception.

        Notes:
            A job is completed when it finishes running due to success or failure. This method will wait for
            any of these events to occur. It's a user responsibility to ensure his job is not programmed in a
            way that makes it run forever.
        """

        import time
        from foundations_contrib.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self.is_job_complete():
            if log_output:
                log.info("waiting for job `" + self.job_name() + "` to finish")
            time.sleep(wait_seconds)

        if log_output:
            log.info("job `" + self.job_name() + "` completed")

    def get_job_status(self):
        """
        Similar to is_job_complete, but with more information

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            status {string} -- String, which is either "Queued", "Running", "Completed", or "Error"

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.get_job_status()

    def get_true_job_status(self):
        """
        Similar to get_job_status, but with more information

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            status {string} -- String, which is either "Queued", "Running", "Completed", or "Error"

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.get_true_job_status()

    def get_job_logs(self):
        """
        Get stdout log for job deployed with SSH job deployment

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            log {string} -- String, which is the contents of the stdout log stream
            
        Raises:
            - This method doesn't raise any exception.
        """

        if not hasattr(self._deployment, 'get_job_logs'):
            return 'Current deployment method does not support get_job_logs()'
        return self._deployment.get_job_logs()

    def stream_job_logs(self):
        if not hasattr(self._deployment, 'stream_job_logs'):
            raise NotImplementedError('Current deployment method does not support stream_job_logs()')
        return self._deployment.stream_job_logs()