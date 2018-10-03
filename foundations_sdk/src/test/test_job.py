"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.job import Job


class TestJob(unittest.TestCase):

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.pipeline import Pipeline

        self._context = PipelineContext()
        self._pipeline = Pipeline(self._context)
        self._stage = self._pipeline.stage(self._method)
    
    def test_run_saves_provenance_run_data(self):
        job = Job(self._stage, hello='world')
        job.run()
        self.assertEqual(self._context.provenance.job_run_data, {'hello': 'world'})
    
    def test_run_saves_provenance_run_data_different_data(self):
        job = Job(self._stage, layers=99, neurons_per_layer=9999)
        job.run()
        self.assertEqual(self._context.provenance.job_run_data, {'layers': 99, 'neurons_per_layer': 9999})

    def _method(self, **kwargs):
        pass