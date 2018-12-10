"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest
from mock import patch
from foundations_contrib.models.pipeline_context_listing import PipelineContextListing


class TestPipelineContextListing(unittest.TestCase):

    class Archiver(object):

        def __init__(self, pipeline_name):
            self._pipeline_name = pipeline_name

        def pipeline_name(self):
            return self._pipeline_name

    class Fetch(object):

        def __init__(self):
            self.archivers = []

        def fetch_archivers(self):
            return self.archivers

    class FetchWrapper(object):
        def __init__(self, fetch):
            self._fetch = fetch

        def __enter__(self):
            return self._fetch

        def __exit__(self, exception_type, exception_value, traceback):
            pass

    class MockPipelineContext(object):
        def __init__(self, archive):
            self.archive = archive

    def setUp(self):
        self._fetch = self.Fetch()
        self._wrapper = self.FetchWrapper(self._fetch)

    @patch('foundations.job_persister.JobPersister.load_archiver_fetch')
    def test_yield_an_empty_list(self, mock):
        mock.return_value = self._wrapper
        self.assertEqual([], self._contexts())

    @patch('foundations.job_persister.JobPersister.load_archiver_fetch')
    @patch('foundations_contrib.models.pipeline_context_with_archive.PipelineContextWithArchive', MockPipelineContext)
    def test_yield_a_single_context_with_an_archiver(self, mock_fetch):
        mock_fetch.return_value = self._wrapper
        archiver = self.Archiver('my job')
        self._fetch.archivers = [archiver]

        pipeline_name, context = self._contexts()[0]

        self.assertEqual('my job', pipeline_name)
        self.assertEqual(archiver, context.archive)

    @patch('foundations.job_persister.JobPersister.load_archiver_fetch')
    @patch('foundations_contrib.models.pipeline_context_with_archive.PipelineContextWithArchive', MockPipelineContext)
    def test_yield_a_single_context_with_an_archiver_different_job(self, mock_fetch):
        mock_fetch.return_value = self._wrapper
        archiver = self.Archiver('my different job')
        self._fetch.archivers = [archiver]

        pipeline_name, context = self._contexts()[0]

        self.assertEqual('my different job', pipeline_name)
        self.assertEqual(archiver, context.archive)

    @patch('foundations.job_persister.JobPersister.load_archiver_fetch')
    @patch('foundations_contrib.models.pipeline_context_with_archive.PipelineContextWithArchive', MockPipelineContext)
    def test_yield_a_single_context_with_multiple_archivers(self, mock_fetch):
        mock_fetch.return_value = self._wrapper
        archiver = self.Archiver('my job')
        archiver2 = self.Archiver('my different job')
        self._fetch.archivers = [archiver, archiver2]

        results = self._contexts()
        results_with_contexts = [(job_id, context.archive)
                                 for job_id, context in results]

        self.assertEqual(
            [('my job', archiver), ('my different job', archiver2)], results_with_contexts)

    def _contexts(self):
        return list(PipelineContextListing.pipeline_contexts())
