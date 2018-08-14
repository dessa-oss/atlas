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
      
      def set_uuid(self, uuid):
        self.uuid = uuid


    class MockResultSaver(object):
          
      def __init__(self):
        self.file_name = None
        self.context = None
        
      def save(self, file_name, context):
        self.file_name = file_name
        self.context = context

    class MockArchive(object):
        
      def __init__(self):
        self.stage_keys = None
        self.archive_provenance = None
        self.uuid = None
        self.stage_repeats = 0
      
      def append_tracker(self):
        return None
      
      def append_miscellaneous(self, stage_listing, stage_keys):
        self.stage_keys = stage_keys
      
      def append_stage_log(self, uuid, stage_log):
        pass
      
      def append_stage_persisted_data(self, uuid, stage_output):
        pass
      
      def append_stage_model_data(self, uuid, model_data):
        pass
      
      def append_stage_miscellaneous(self, uuid, stage_context, archive_stage_context):
        pass
      
      def append_provenance(self, archive_provenance):
        self.archive_provenance = archive_provenance
      
      def fetch_stage_log(self, uuid):
        self.uuid = uuid
        self.stage_repeats += 1
        return self.uuid
      
      def fetch_stage_miscellaneous(self, uuid, archive_type):
        pass
      
      def fetch_miscellaneous(self, stage_listing):
        pass

      def fetch_stage_persisted_data(self, uuid):
        self.uuid = uuid
        return self.uuid
      
      def fetch_stage_model_data(self, uuid):
        self.uuid = uuid
        return self.uuid

      def fetch_provenance(self):
        pass

        

    
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
      mock_pipeline.set_uuid('9sdf9')

      pipeline_context.add_stage_context(mock_pipeline)
      self.assertEqual({'9sdf9': mock_pipeline}, pipeline_context.stage_contexts)

    def test_add_stage_context_with_multiple_stages(self):
      pipeline_context = PipelineContext()

      mock_pipeline = self.MockPipeline()
      mock_pipeline.set_uuid('9sdf9')
      
      mock_pipeline_two = self.MockPipeline()
      mock_pipeline_two.set_uuid('s9d0f')

      pipeline_context.add_stage_context(mock_pipeline)
      pipeline_context.add_stage_context(mock_pipeline_two)
      self.assertEqual({'s9d0f': mock_pipeline_two, '9sdf9': mock_pipeline}, pipeline_context.stage_contexts)

    def test_add_stage_context_add_stage_twice(self):
      pipeline_context = PipelineContext()

      mock_pipeline = self.MockPipeline()
      mock_pipeline.set_uuid('9sdf9')

      pipeline_context.add_stage_context(mock_pipeline)
      pipeline_context.add_stage_context(mock_pipeline)
      self.assertEqual({'9sdf9': mock_pipeline}, pipeline_context.stage_contexts)

    def test_fill_provenance(self):
      from foundations.config_manager import ConfigManager
      self.config_manager = ConfigManager()
      pipeline_context = PipelineContext()

      self.config_manager['other_world'] = 'aliens'
      config_return = {'other_world': 'aliens'}

      pipeline_context.fill_provenance(self.config_manager)
      self.assertEqual(pipeline_context.provenance.config, config_return)

    def test_save_uses_save_method_on_result_saver(self):
      pipeline_context = PipelineContext()
      mock_result_saver = self.MockResultSaver()

      pipeline_context.save(mock_result_saver)
      self.assertEqual(mock_result_saver.file_name, pipeline_context.file_name)
      self.assertEqual(mock_result_saver.context, pipeline_context._context())

    def test_save_to_archive_is_able_to_call_all_needed_archive_methods(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.save_to_archive(mock_archive)
      self.assertEqual([], mock_archive.stage_keys)

    def test_load_stage_log_from_archive_able_to_call_all_methods(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.load_stage_log_from_archive(mock_archive)
      self.assertEqual(pipeline_context.global_stage_context.stage_log, mock_archive.uuid)
    
    def test_load_stage_log_from_archive_updates_already_loaded_flag_on_run(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.load_stage_log_from_archive(mock_archive)
      self.assertFalse(0, mock_archive.stage_repeats)

    
    def test_load_persisted_data_from_archive_able_to_set_stage_output(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.load_persisted_data_from_archive(mock_archive)
      self.assertEqual(pipeline_context.global_stage_context.stage_output, mock_archive.uuid)
    
    def test_load_persisted_data_from_archive_able_to_set_model_data(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.load_persisted_data_from_archive(mock_archive)
      self.assertEqual(pipeline_context.global_stage_context.model_data, mock_archive.uuid)

    def test_load_persisted_data_from_archive_updates_already_loaded_flag_on_run(self):
      pipeline_context = PipelineContext()
      mock_archive = self.MockArchive()

      pipeline_context.load_persisted_data_from_archive(mock_archive)
      self.assertEqual(0, mock_archive.stage_repeats)

    
    # def test_load_provenance_from_archive(self):
    #   pipeline_context = PipelineContext()
    #   mock_archive = self.MockArchive()

    #   pipeline_context.load_provenance_from_archive(mock_archive)
    #   self.assertEqual()