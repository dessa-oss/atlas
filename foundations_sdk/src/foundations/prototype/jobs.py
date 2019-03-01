"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_queued_jobs():
    from pandas import DataFrame
    from foundations_contrib.models.queued_job import QueuedJob

    job_attributes = [job.attributes for job in QueuedJob.all()]

    return DataFrame(job_attributes)

def cancel_queued_jobs(job_list):
    return {job_id: False for job_id in job_list}