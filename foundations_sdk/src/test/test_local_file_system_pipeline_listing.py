"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.local_file_system_pipeline_listing import LocalFileSystemPipelineListing


class TestLocalFileSystemPipelineListing(unittest.TestCase):

    def test_tracks_pipeline(self):
        path = self._make_path()
        listing = LocalFileSystemPipelineListing(path)
        listing.track_pipeline('some_pipeline')
        with self._open_listing_file(path, 'some_pipeline.tracker') as file:
            self.assertEqual(b'some_pipeline', file.read())

    def test_tracks_pipeline_different_name(self):
        path = self._make_path()
        listing = LocalFileSystemPipelineListing(path)
        listing.track_pipeline('some_other_pipeline')
        with self._open_listing_file(path, 'some_other_pipeline.tracker') as file:
            self.assertEqual(b'some_other_pipeline', file.read())

    def test_get_pipeline_names_returns_empty(self):
        path = self._make_path()
        listing = LocalFileSystemPipelineListing(path)
        self.assertEqual([], listing.get_pipeline_names())

    def test_get_pipeline_names_returns_a_pipeline(self):
        path = self._make_path()
        listing = LocalFileSystemPipelineListing(path)
        listing.track_pipeline('some_pipeline')
        self.assertEqual(['some_pipeline'], listing.get_pipeline_names())

    def test_get_pipeline_names_returns_multiple_pipelines(self):
        path = self._make_path()
        listing = LocalFileSystemPipelineListing(path)
        listing.track_pipeline('some_pipeline')
        listing.track_pipeline('some_other_pipeline')
        self.assertEqual(set(['some_pipeline', 'some_other_pipeline']), set(
            listing.get_pipeline_names()))

    def _open_listing_file(self, path, name):
        from os.path import join
        return open(join(path, name), 'rb')

    def _make_path(self):
        from uuid import uuid4
        return '/tmp/{}'.format(uuid4())
