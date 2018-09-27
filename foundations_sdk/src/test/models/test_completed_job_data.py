"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.models.completed_job_data import CompletedJobData


class TestCompletedJobData(unittest.TestCase):

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

    def setUp(self):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext
        from foundations.global_state import config_manager
        from foundations.bucket_pipeline_archive import BucketPipelineArchive

        self._listing = self.MockArchiveListing()

        def get_listing():
            return self._listing

        self._bucket = self.MemoryBucket()

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

    def tearDown(self):
        from foundations.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def test_returns_a_job(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._make_and_persist_job('my job', stage, 9999999999, 9999999999)

        job = CompletedJobData(
            self._make_wrapped_context(), 'my job').load_job()
        expected_job = {
            'job_id': 'my job',
            'user': 'Unspecified',
            'job_parameters': {},
            'input_params': [],
            'output_metrics': {'loss': 15.33},
            'status': 'Completed',
            'start_time': 9999999999,
            'completed_time': 9999999999
        }
        self.assertEqual(expected_job, job)

    def test_returns_a_job_different_name(self):
        def method():
            pass

        stage = self._pipeline.stage(method)

        self._make_and_persist_job('my other job', stage, 123232233, 312333333)

        job = CompletedJobData(
            self._make_wrapped_context(), 'my other job').load_job()
        expected_job = {
            'job_id': 'my other job',
            'user': 'Unspecified',
            'job_parameters': {},
            'input_params': [],
            'output_metrics': {},
            'status': 'Completed',
            'start_time': 123232233,
            'completed_time': 312333333
        }
        self.assertEqual(expected_job, job)

    def test_returns_a_job_different_metrics(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('win', 99.9)
            log_metric('accuracy', 0)

        stage = self._pipeline.stage(method)

        self._make_and_persist_job('my job', stage, 444444, 5555555)

        job = CompletedJobData(
            self._make_wrapped_context(), 'my job').load_job()
        expected_job = {
            'job_id': 'my job',
            'user': 'Unspecified',
            'job_parameters': {},
            'input_params': [],
            'output_metrics': {'win': 99.9, 'accuracy': 0},
            'status': 'Completed',
            'start_time': 444444,
            'completed_time': 5555555
        }
        self.assertEqual(expected_job, job)

    def test_returns_a_job_metric_multiple_instances(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('win', 99.9)
            log_metric('win', 99.99)

        stage = self._pipeline.stage(method)

        self._make_and_persist_job('my job', stage, 444444, 5555555)

        job = CompletedJobData(
            self._make_wrapped_context(), 'my job').load_job()
        expected_job = {
            'job_id': 'my job',
            'user': 'Unspecified',
            'job_parameters': {},
            'input_params': [],
            'output_metrics': {'win': [99.9, 99.99]},
            'status': 'Completed',
            'start_time': 444444,
            'completed_time': 5555555
        }
        self.assertEqual(expected_job, job)

    def test_returns_a_job_with_run_data(self):
        from foundations.hyperparameter import Hyperparameter

        def method(hello):
            pass

        stage = self._pipeline.stage(method, hello=Hyperparameter('hello'))

        self._make_and_persist_job(
            'my job', stage, 343433, 43444, hello='world')

        job = CompletedJobData(
            self._make_wrapped_context(), 'my job').load_job()
        input_params = [{'stage_uuid': 'e56573879d1a601ec8845955e194dff00942bf30',
                         'name': 'hello', 'value': {'type': 'dynamic', 'name': 'hello'}}]
        expected_job = {
            'job_id': 'my job',
            'user': 'Unspecified',
            'job_parameters': {'hello': 'world'},
            'input_params': input_params,
            'output_metrics': {},
            'status': 'Completed',
            'start_time': 343433,
            'completed_time': 43444,
        }
        self.assertEqual(expected_job, job)

    def _make_and_persist_job(self, job_name, stage, start_time, end_time, **job_parameters):
        from foundations.job import Job
        from foundations.job_persister import JobPersister

        self._pipeline_context.file_name = job_name
        self._pipeline_context.global_stage_context.start_time = start_time

        job = Job(stage, **job_parameters)
        job.run()

        self._pipeline_context.global_stage_context.end_time = end_time
        JobPersister(job).persist()

    def _make_wrapped_context(self):
        from foundations.job_persister import JobPersister
        from foundations.models.pipeline_context_with_archive import PipelineContextWithArchive

        with JobPersister.load_archiver_fetch() as fetch:
            archiver = list(fetch.fetch_archivers())[0]
            return PipelineContextWithArchive(archiver)
