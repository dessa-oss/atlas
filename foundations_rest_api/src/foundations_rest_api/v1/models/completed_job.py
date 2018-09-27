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
    def all():
        from foundations_rest_api.response import Response
        return Response('CompletedJob', CompletedJob._all_internal)

    @staticmethod
    def _all_internal():
        return list(CompletedJob._load_jobs())

    @staticmethod
    def _load_jobs():
        from foundations.models.pipeline_context_listing import PipelineContextListing

        for job_id, context in PipelineContextListing.pipeline_contexts():
            job_properties = CompletedJob._job_properties(context, job_id)
            yield CompletedJob(**job_properties)

    @staticmethod
    def _job_properties(context, job_id):
        from foundations.models.completed_job_data import CompletedJobData

        properties = CompletedJobData(context, job_id).load_job()
        properties['start_time'] = CompletedJob._datetime_string(properties['start_time'])
        properties['completed_time'] = CompletedJob._datetime_string(properties['completed_time'])
        del properties['project_name']
        return properties

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        date_time = datetime.utcfromtimestamp(time)
        return str(date_time)
