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
        result = []

        for job_id, context in CompletedJob.contexts():
            stage_metrics = {}
            for stage_context in context.stage_contexts.values():
                for item in stage_context.stage_log:
                    CompletedJob._add_metric(stage_metrics, item['key'], item['value'])

            job = CompletedJob(
                job_id=job_id, user='Unspecified',
                job_parameters=context.provenance.job_run_data, 
                output_metrics=stage_metrics, 
                status='Completed',
                start_time=CompletedJob._datetime_string(context.global_stage_context.start_time),
                completed_time=CompletedJob._datetime_string(context.global_stage_context.end_time)
            )
            result.append(job)

        return result

    @staticmethod
    def _add_metric(metrics, key, value):
        if key in metrics:
            if isinstance(metrics[key], list):
                metrics[key].append(value)
            else:
                metrics[key] = [metrics[key], value]
        else:
            metrics[key] = value


    @staticmethod
    def contexts():
        from foundations.job_persister import JobPersister

        with JobPersister.load_archiver_fetch() as archiver_fetch:
            for archiver in archiver_fetch.fetch_archivers():
                yield archiver.pipeline_name(), CompletedJob.load_context(archiver)

    @staticmethod
    def load_context(archiver):
        from foundations.pipeline_context import PipelineContext

        context = PipelineContext()
        context.load_stage_log_from_archive(archiver)
        context.load_provenance_from_archive(archiver)

        return context

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        date_time = datetime.utcfromtimestamp(time)
        return str(date_time)
