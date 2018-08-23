"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.foundations_context import FoundationsContext


class TestFoundationsContext(unittest.TestCase):

    def setUp(self):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)
        self._context = FoundationsContext(self._pipeline)

    def test_pipeline(self):
        self.assertEqual(self._pipeline, self._context.pipeline())

    def test_pipeline_context(self):
        self.assertEqual(self._pipeline_context, self._context.pipeline_context())

    def test_change_pipeline_changes_pipeline(self):
        from foundations.pipeline import Pipeline

        new_pipeline = Pipeline(self._pipeline_context)
        with self._context.change_pipeline(new_pipeline):
            self.assertEqual(new_pipeline, self._context.pipeline())

    def test_change_logger_resets_logger(self):
        from foundations.pipeline import Pipeline

        new_pipeline = Pipeline(self._pipeline_context)
        with self._context.change_pipeline(new_pipeline):
            pass
        self.assertEqual(self._pipeline, self._context.pipeline())