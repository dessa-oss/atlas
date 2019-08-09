"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobsTestsHelperMixin(object):

    def _setup_deployment(self, expected_status):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.global_state import deployment_manager
        from .mocks.scheduler_backend import MockSchedulerBackend
        from .mocks.deployment import MockDeployment

        deployment_manager._scheduler = None
        self._scheduler_backend_instance = MockSchedulerBackend(
            expected_status, [])
        self._mock_deployment = MockDeployment(self._scheduler_backend)

        config_manager['deployment_implementation'] = {
            'deployment_type': self._mock_deployment,
        }

    def _setup_results_archiving(self):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
        from .mocks.archive_listing import MockArchiveListing
        from .mocks.memory_bucket import MemoryBucket

        self._listing = MockArchiveListing()

        def get_listing():
            return self._listing

        self._bucket = MemoryBucket()

        def get_bucket():
            return self._bucket

        config_manager['archive_listing_implementation'] = {
            'archive_listing_type': get_listing
        }
        archive_implementation = {
            'archive_type': BucketPipelineArchive,
            'constructor_arguments': [get_bucket],
        }
        config_manager['stage_log_archive_implementation'] = archive_implementation
        config_manager['persisted_data_archive_implementation'] = archive_implementation
        config_manager['provenance_archive_implementation'] = archive_implementation
        config_manager['job_source_archive_implementation'] = archive_implementation
        config_manager['artifact_archive_implementation'] = archive_implementation
        config_manager['miscellaneous_archive_implementation'] = archive_implementation

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)

    def _cleanup(self):
        from foundations_contrib.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def _scheduler_backend(self):
        return self._scheduler_backend_instance

    def _make_completed_job(self, job_name, stage, start_time, end_time, **job_parameters):
        from foundations.job import Job
        from foundations.job_persister import JobPersister

        self._pipeline_context.file_name = job_name
        self._pipeline_context.global_stage_context.start_time = start_time

        job = Job(stage, **job_parameters)
        job.run()

        self._pipeline_context.global_stage_context.end_time = end_time
        JobPersister(job).persist()

    def _make_scheduled_job(self, job_name, start_timestamp, duration_timestamp, user, state):
        from foundations.scheduler_job_information import JobInformation

        job_information = JobInformation(
            job_name, start_timestamp, duration_timestamp, state, user)
        self._scheduler_backend_instance._job_information.append(
            job_information)

    def _make_running_job(self, job_name, start_timestamp, duration_timestamp, user):
        return self._make_scheduled_job(job_name, start_timestamp, duration_timestamp, user, 'RUNNING')

    def _make_queued_job(self, job_name, start_timestamp, duration_timestamp, user):
        return self._make_scheduled_job(job_name, start_timestamp, duration_timestamp, user, 'QUEUED')
