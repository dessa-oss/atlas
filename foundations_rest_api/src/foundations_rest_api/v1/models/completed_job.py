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
        from foundations.models.completed_job_data import CompletedJobData

        result = []

        for job_id, context in CompletedJob.contexts():
            job_properties = CompletedJobData(context, job_id).load_job()
            job_properties['start_time'] = CompletedJob._datetime_string(job_properties['start_time'])
            job_properties['completed_time'] = CompletedJob._datetime_string(job_properties['completed_time'])
            job = CompletedJob(**job_properties)
            result.append(job)

        return result



    @staticmethod
    def contexts():
        from foundations.job_persister import JobPersister

        with JobPersister.load_archiver_fetch() as archiver_fetch:
            for archiver in archiver_fetch.fetch_archivers():
                yield archiver.pipeline_name(), CompletedJob.load_context(archiver)

    @staticmethod
    def load_context(archiver):
        from foundations.models.pipeline_context_with_archive import PipelineContextWithArchive
        return PipelineContextWithArchive(archiver)

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        date_time = datetime.utcfromtimestamp(time)
        return str(date_time)
