"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.bucket_pipeline_listing import BucketPipelineListing


class TestBucketPipelineListing(unittest.TestCase):

    class MockBucket(object):

        def __init__(self):
            self.data = {}

        def upload_from_string(self, name, value):
            self.data[name] = value

        def download_as_string(self, name):
            return self.data.get(name)

        def list_files(self, pathname):
            from fnmatch import fnmatch
            return filter(lambda path: fnmatch(path, pathname), self.data.keys())

    def setUp(self):
        self._mocked_bucket = self.MockBucket()

    def test_tracks_pipeline(self):
        listing = BucketPipelineListing(self._mock_bucket)
        listing.track_pipeline('some_pipeline')
        self.assertEqual(
            'some_pipeline', self._mocked_bucket.data['some_pipeline.tracker'])

    def test_tracks_pipeline_different_name(self):
        listing = BucketPipelineListing(self._mock_bucket)
        listing.track_pipeline('some_other_pipeline')
        self.assertEqual(
            'some_other_pipeline', self._mocked_bucket.data['some_other_pipeline.tracker'])

    def test_get_pipeline_names_returns_empty(self):
        listing = BucketPipelineListing(self._mock_bucket)
        self.assertEqual([], listing.get_pipeline_names())

    def test_get_pipeline_names_returns_a_pipeline(self):
        listing = BucketPipelineListing(self._mock_bucket)
        listing.track_pipeline('some_pipeline')
        self.assertEqual(['some_pipeline'], listing.get_pipeline_names())

    def test_get_pipeline_names_returns_multiple_pipelines(self):
        listing = BucketPipelineListing(self._mock_bucket)
        listing.track_pipeline('some_pipeline')
        listing.track_pipeline('some_other_pipeline')
        self.assertEqual(set(['some_pipeline', 'some_other_pipeline']), set(listing.get_pipeline_names()))

    def _mock_bucket(self):
        return self._mocked_bucket
