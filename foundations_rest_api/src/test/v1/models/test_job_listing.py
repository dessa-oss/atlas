"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from foundations_rest_api.v1.models.job import Job
from foundations.scheduler_legacy_backend import LegacyBackend

class TestJob(unittest.TestCase):

    class MockArchiveListing(object):

        def __init__(self):
            self._listing = []

        def track_pipeline(self, name):
            self._listing.append(name)

        def get_pipeline_names(self):
            return self._listing

    class MemoryBucket(object):

        def __init__(self):
            self._bucket = {}

        def upload_from_string(self, name, data):
            self._bucket[name] = data

        def upload_from_file(self, name, input_file):
            self._bucket[name] = input_file.read()

        def exists(self, name):
            return name in self._bucket

        def download_as_string(self, name):
            return self._bucket[name]

        def download_to_file(self, name, output_file):
            output_file.write(self._bucket[name])
            output_file.flush()
            output_file.seek(0)

        def list_files(self, pathname):
            return self._bucket.keys()

        def remove(self, name):
            del self._bucket[name]

        def move(self, source, destination):
            value = self.download_as_string(source)
            self.remove(source)
            self.upload_from_string(destination, value)

    class MockSchedulerBackend(LegacyBackend):

        def __init__(self, expected_status, job_information):
            self._expected_status = expected_status
            self._job_information = job_information

        def get_paginated(self, start_index, number_to_get, status):
            if self._expected_status == status:
                return self._job_information

            return []

    class MockDeployment(object):

        def __init__(self, scheduler_backend_callback):
            self._scheduler_backend_callback = scheduler_backend_callback

        def scheduler_backend(self):
            return self._scheduler_backend_callback

    def setUp(self):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext
        from foundations.global_state import config_manager, deployment_manager
        from foundations.bucket_pipeline_archive import BucketPipelineArchive

        self._listing = self.MockArchiveListing()

        def get_listing():
            return self._listing

        self._bucket = self.MemoryBucket()

        def get_bucket():
            return self._bucket

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)

        self._scheduler_backend_instance = self.MockSchedulerBackend('RUNNING', [])
        self._mock_deployment = self.MockDeployment(self._scheduler_backend)

        deployment_manager._scheduler = None # ugh...
        
        config_manager['deployment_implementation'] = {
            'deployment_type': self._mock_deployment
        }

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

    def _scheduler_backend(self):
        return self._scheduler_backend_instance

    def tearDown(self):
        from foundations.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = Job(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = Job(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = Job(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_job_parameters(self):
        job = Job(job_parameters={'a': 5})
        self.assertEqual({'a': 5}, job.job_parameters)

    def test_has_job_parameters_different_params(self):
        job = Job(job_parameters={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.job_parameters)

    def test_has_input_params(self):
        job = Job(input_params=['some list of parameters'])
        self.assertEqual(['some list of parameters'], job.input_params)

    def test_has_input_params_different_params(self):
        job = Job(input_params=['some different list of parameters'])
        self.assertEqual(['some different list of parameters'], job.input_params)

    def test_has_output_metrics(self):
        job = Job(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)

    def test_has_output_metrics_different_params(self):
        job = Job(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)

    def test_has_status_completed(self):
        job = Job(status='completed')
        self.assertEqual('completed', job.status)

    def test_has_status_running(self):
        job = Job(status='running')
        self.assertEqual('running', job.status)

    def test_has_status_different_params(self):
        job = Job(status='completed in error')
        self.assertEqual('completed in error', job.status)

    def test_has_start_time(self):
        job = Job(start_time=123423423434)
        self.assertEqual(123423423434, job.start_time)

    def test_has_start_time_different_params(self):
        job = Job(start_time=884234222323)
        self.assertEqual(884234222323, job.start_time)

    def test_has_completed_time(self):
        job = Job(completed_time=123423423434)
        self.assertEqual(123423423434, job.completed_time)

    def test_has_completed_time_none(self):
        job = Job(completed_time=None)
        self.assertIsNone(job.completed_time)

    def test_has_completed_time_different_params(self):
        job = Job(completed_time=884234222323)
        self.assertEqual(884234222323, job.completed_time)

    def test_all_returns_multiple_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000000', 
            user='soju hero', 
            start_time='1973-11-29T21:33:09', 
            job_parameters={},
            input_params=[], 
            output_metrics={},
            status='Running',
            completed_time=None
        )

        expected_job_2 = Job(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )


        result = Job.all().evaluate()
        expected_jobs = [expected_job_2, expected_job_1]
        self.assertEqual(expected_jobs, result)

    def test_all_returns_jobs_filtered_by_project(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._pipeline_context.provenance.project_name = 'project 1'
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000001', 123456789, 9999, 'soju hero')

        self._pipeline_context.provenance.project_name = 'project 2'
        self._make_running_job('00000000-0000-0000-0000-000000000002', 987654321, 8888, 'quin lin')

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000001', 
            user='soju hero', 
            start_time='1973-11-29T21:33:09', 
            job_parameters={},
            input_params=[], 
            output_metrics={},
            status='Running',
            completed_time=None
        )

        expected_job_2 = Job(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )

        result = Job.all(project_name='project 1').evaluate()
        expected_jobs = [expected_job_2, expected_job_1]
        self.assertEqual(len(result), 2)
        self.assertEqual(expected_jobs, result)

    def _make_completed_job(self, job_name, stage, start_time, end_time, **job_parameters):
        from foundations.job import Job
        from foundations.job_persister import JobPersister

        self._pipeline_context.file_name = job_name
        self._pipeline_context.global_stage_context.start_time = start_time

        job = Job(stage, **job_parameters)
        job.run()

        self._pipeline_context.global_stage_context.end_time = end_time
        JobPersister(job).persist()

    def _make_running_job(self, job_name, start_timestamp, duration_timestamp, user):
        from foundations.scheduler_job_information import JobInformation

        job_information = JobInformation(job_name, start_timestamp, duration_timestamp, 'RUNNING', user)
        self._scheduler_backend_instance._job_information.append(job_information)