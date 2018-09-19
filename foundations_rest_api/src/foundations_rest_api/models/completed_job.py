"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.models.property_model import PropertyModel


class CompletedJob(PropertyModel):

    job_id = PropertyModel.define_property()
    user = PropertyModel.define_property()
    input_params = PropertyModel.define_property()
    output_metrics = PropertyModel.define_property()
    status = PropertyModel.define_property()

    @staticmethod
    def all():
        from foundations_rest_api.response import Response
        return Response('CompletedJob', CompletedJob._all_internal)

    @staticmethod
    def _all_internal():
        from foundations.job_persister import JobPersister
        from foundations.pipeline_context import PipelineContext

        result = []

        with JobPersister.load_archiver_fetch() as archiver_fetch:
            for archiver in archiver_fetch.fetch_archivers():
                context = PipelineContext()
                context.load_stage_log_from_archive(archiver)
                context.load_provenance_from_archive(archiver)

                stage_metrics = {}
                for stage_context in context.stage_contexts.values():
                    for item in stage_context.stage_log:
                        stage_metrics[item['key']] = item['value']

                job = CompletedJob(job_id=archiver.pipeline_name(), user='Unspecified',
                                   input_params=context.provenance.job_run_data, output_metrics=stage_metrics, status='Completed')
                result.append(job)

        return result
