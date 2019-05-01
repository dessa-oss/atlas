"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec import *
from foundations_internal.foundations_context import FoundationsContext


class TestFoundationsContext(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    def setUp(self):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)
        self._context = FoundationsContext(self._pipeline)

    def test_pipeline(self):
        self.assertEqual(self._pipeline, self._context.pipeline())

    def test_pipeline_context(self):
        self.assertEqual(self._pipeline_context,
                         self._context.pipeline_context())

    def test_change_pipeline_changes_pipeline(self):
        from foundations_internal.pipeline import Pipeline

        new_pipeline = Pipeline(self._pipeline_context)
        with self._context.change_pipeline(new_pipeline):
            self.assertEqual(new_pipeline, self._context.pipeline())

    def test_change_logger_resets_logger(self):
        from foundations_internal.pipeline import Pipeline

        new_pipeline = Pipeline(self._pipeline_context)
        with self._context.change_pipeline(new_pipeline):
            pass
        self.assertEqual(self._pipeline, self._context.pipeline())

    def test_set_project_name_sets_provenance_project_name(self):
        self._context.set_project_name('my project')
        self.assertEqual(
            'my project', self._pipeline_context.provenance.project_name)

    def test_set_project_name_sets_provenance_project_name_different_name(self):
        self._context.set_project_name('my other project')
        self.assertEqual('my other project',
                         self._pipeline_context.provenance.project_name)

    def test_get_job_id(self):
        self._pipeline_context.file_name = self.job_id
        self.assertEqual(self.job_id, self._context.job_id())

    def test_pickle_getstate_raises_exception(self):
        with self.assertRaises(ValueError) as error_context:
            self._context.__getstate__()
        self.assertIn('FoundationsContexts do not support serialization', error_context.exception.args)

    def test_pickle_setstate_raises_exception(self):
        with self.assertRaises(ValueError) as error_context:
            self._context.__setstate__({})
        self.assertIn('FoundationsContexts do not support serialization', error_context.exception.args)

    def test_is_unserializable(self):
        import pickle

        with self.assertRaises(ValueError) as error_context:
            pickle.dumps(self._context)

        self.assertIn('FoundationsContexts do not support serialization', error_context.exception.args)
