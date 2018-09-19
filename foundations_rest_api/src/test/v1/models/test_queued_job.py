"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.queued_job import QueuedJob


class TestQueuedJob(unittest.TestCase):

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

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = QueuedJob(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = QueuedJob(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = QueuedJob(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_submitted_time(self):
        job = QueuedJob(submitted_time=484848448448844)
        self.assertEqual(484848448448844, job.submitted_time)

    def test_has_submitted_time_different_params(self):
        job = QueuedJob(submitted_time=984222255555546)
        self.assertEqual(984222255555546, job.submitted_time)

    def test_all_is_empty_response(self):
        self.assertEqual([], QueuedJob.all().evaluate())