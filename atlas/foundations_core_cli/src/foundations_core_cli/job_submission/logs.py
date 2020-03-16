
def stream_job_logs(deployment):
    from foundations_contrib.global_state import log_manager
    from os import environ
    import time
    
    logger = log_manager.get_logger(__name__)
    if environ.get('DISABLE_LOG_STREAMING', 'False') == 'False':
        logger.info('Job queued. Ctrl-C to stop streaming - job will not be interrupted or cancelled.')
        job_running = False

        time.sleep(1)

        try:
            for item in deployment.stream_job_logs():
                if not job_running:
                    logger.info('Job running, streaming logs.')
                    job_running = True
                if 'RuntimeError' in item:
                    import sys
                    sys.exit(item)
                print(item)

            try:
                counter = 0
                timeout = 15
                job_status = deployment.get_true_job_status()

                while (job_status == 'running' or job_status is None) and counter < timeout:
                    time.sleep(1)
                    counter += 1
                    job_status = deployment.get_true_job_status()

                if job_status == 'failed':
                    logger.error("Job '{}' has failed.".format(deployment.job_name()))
                elif job_status == 'completed':
                    logger.info("Job '{}' has completed.".format(deployment.job_name()))
                elif job_status == 'running':
                    logger.info("Job '{}' is running, see GUI for full logs and status.".format(deployment.job_name()))
                else:
                    logger.warning("Job status of job '{}' is unknown.".format(deployment.job_name()))
            except AttributeError:
                logger.info("Job '{}' has finished.".format(deployment.job_name()))

        except TimeoutError:
            logger.info('Job cannot be found. Possibly because it has been removed from the queue.')
