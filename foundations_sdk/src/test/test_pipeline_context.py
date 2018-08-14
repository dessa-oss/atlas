"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.pipeline_context import PipelineContext


class TestPipelineContext(unittest.TestCase):

    class MockPipeline(object):
      def __init__(self):
        self.uuid = None
      
      def set_uuid(self):
        self.uuid = '9sdf9'

    def setUp(self):
        from foundations.config_manager import ConfigManager
        self.config_manager = ConfigManager()
    
    def test_mark_fully_loaded(self):
      pipeline_context = PipelineContext()
      
      self.assertFalse(pipeline_context._stage_log_archive_loaded)
      self.assertFalse(pipeline_context._persisted_data_archive_loaded)
      self.assertFalse(pipeline_context._provenance_archive_loaded)
      self.assertFalse(pipeline_context._job_source_archive_loaded)
      self.assertFalse(pipeline_context._artifact_archive_loaded)
      self.assertFalse(pipeline_context._miscellaneous_archive_loaded)
      
      pipeline_context.mark_fully_loaded()
      
      self.assertTrue(pipeline_context._stage_log_archive_loaded)
      self.assertTrue(pipeline_context._persisted_data_archive_loaded)
      self.assertTrue(pipeline_context._provenance_archive_loaded)
      self.assertTrue(pipeline_context._job_source_archive_loaded)
      self.assertTrue(pipeline_context._artifact_archive_loaded)
      self.assertTrue(pipeline_context._miscellaneous_archive_loaded)
    
    def test_add_stage_context(self):
      pipeline_context = PipelineContext()

      mock_pipeline = self.MockPipeline()
      mock_pipeline.set_uuid()

      pipeline_context.add_stage_context(mock_pipeline)
      self.assertEqual({'9sdf9': mock_pipeline}, pipeline_context.stage_contexts)

    def test_fill_provenance(self): 
      pipeline_context = PipelineContext()

      pipeline_context.fill_provenance(self.config_manager)
