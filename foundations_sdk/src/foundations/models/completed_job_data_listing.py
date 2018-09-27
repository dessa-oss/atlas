"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CompletedJobDataListing(object):
    @staticmethod
    def completed_job_data():
        from foundations.models.pipeline_context_listing import PipelineContextListing
        from foundations.models.completed_job_data import CompletedJobData

        for job_id, context in PipelineContextListing.pipeline_contexts():
            yield CompletedJobData(job_id, context).load_job()