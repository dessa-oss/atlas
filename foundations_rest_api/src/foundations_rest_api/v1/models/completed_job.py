"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.v1.models.property_model import PropertyModel


class CompletedJob(PropertyModel):

    job_id = PropertyModel.define_property()
    user = PropertyModel.define_property()
    job_parameters = PropertyModel.define_property()
    input_params = PropertyModel.define_property()
    output_metrics = PropertyModel.define_property()
    status = PropertyModel.define_property()
    start_time = PropertyModel.define_property()
    completed_time = PropertyModel.define_property()

    @staticmethod
    def all(project_name=None):
        from foundations_rest_api.response import Response

        def _all():
            return CompletedJob._all_internal(project_name)

        return Response('CompletedJob', _all)

    @staticmethod
    def _all_internal(project_name):
        return list(CompletedJob._load_jobs(project_name))

    @staticmethod
    def _load_jobs(project_name):
        from foundations.models.pipeline_context_listing import PipelineContextListing

        completed_jobs = []

        def _loop_body(job_id, context):
            job_properties = CompletedJob._job_properties(context, job_id)
            if project_name is None or project_name == job_properties['project_name']:
                del job_properties['project_name']
                completed_jobs.append(CompletedJob(**job_properties))

        for job_id, context in list(PipelineContextListing.pipeline_contexts()):
            _loop_body(job_id, context)

        return completed_jobs

    @staticmethod
    def _job_properties(context, job_id):
        from foundations.models.completed_job_data import CompletedJobData

        properties = CompletedJobData(context, job_id).load_job()
        properties['start_time'] = CompletedJob._datetime_string(properties['start_time'])
        properties['completed_time'] = CompletedJob._datetime_string(properties['completed_time'])
        return properties

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        if time is None:
            return 'No time available'
        date_time = datetime.utcfromtimestamp(time)
        return date_time.isoformat()
