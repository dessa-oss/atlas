"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def stream_job_logs(deployment):
    from foundations_contrib.global_state import log_manager
    
    logger = log_manager.get_logger(__name__)
    logger.info('Job is queued; Ctrl-C to stop streaming - job will not be interrupted or cancelled')
    job_running = False

    for item in deployment.stream_job_logs():
        if not job_running:
            logger.info('Job is running; streaming logs')
            job_running = True
        print(item)