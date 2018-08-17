"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.stage_context import StageContext


class TestStageContext(unittest.TestCase):

    class MockArchive(object):

        def __init__(self):
            self.archive_provenance = None
            self.archive_stage_context = None
            self.fetch_stage_uuid = None
            self.fetch_persisted_uuid = None
            self.fetch_model_uuid = None

        def append_stage_log(self, uuid, stage_log):
            pass

        def append_stage_persisted_data(self, uuid, stage_output):
            pass

        def append_stage_model_data(self, uuid, model_data):
            pass

        def append_stage_miscellaneous(self, uuid, stage_context, archive_stage_context):
            self.archive_stage_context = archive_stage_context

        def fetch_stage_log(self, uuid):
            return self.fetch_stage_uuid

        def fetch_stage_persisted_data(self, stage_uuid_string):
            return self.fetch_persisted_uuid

        def fetch_stage_model_data(self, stage_uuid_string):
            return self.fetch_model_uuid

        def fetch_stage_miscellaneous(self, stage_uuid_string, name):
            pass

    class MockException(object):

        def mock_output(self):
            import sys
            return sys.exc_info()

    def test_set_stage_output(self):
        stage_context = StageContext()
        stage_context.set_stage_output('some stage output')
        self.assertEqual('some stage output', stage_context.stage_output)

    def test_set_stage_output_has_stage_after_run(self):
        stage_context = StageContext()
        stage_context.set_stage_output('some stage output')
        self.assertTrue(stage_context.has_stage_output)

    def test_set_stage_output_has_none_stage_output(self):
        stage_context = StageContext()
        self.assertIsNone(stage_context.has_stage_output)

    def test_add_error_information(self):
        stage_context = StageContext()

        mock_exception_instance = self.MockException()
        mock_exception = mock_exception_instance.mock_output()

        stage_context.add_error_information(mock_exception)
        self.assertEqual({'type': None, 'exception': None,
                          'traceback': []}, stage_context.error_information)

    def test_save_to_archive_with_specific_values(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.meta_data = {'value': 'one'}
        stage_context.data_uuid = 'sd9f8sdf'
        stage_context.stage_output = 'some output from model'
        stage_context.uuid = '89s7df987sdf7'
        stage_context.error_information = 'an error message'
        stage_context.model_data = 'model data'
        stage_context.start_time = 3289798798732
        stage_context.end_time = 92380982309
        stage_context.delta_time = 398098
        stage_context.is_context_aware = False
        stage_context.used_cache = False
        stage_context.cache_uuid = None
        stage_context.cache_read_time = False
        stage_context.cache_write_time = None
        stage_context.has_stage_output = None
        stage_context.save_to_archive(mock_archive)

        self.assertEqual({
            'cache_read_time': False,
            'cache_uuid': None,
            'cache_write_time': None,
            'data_uuid': 'sd9f8sdf',
            'delta_time': 398098,
            'end_time': 92380982309,
            'error_information': 'an error message',
            'has_stage_output': None,
            'is_context_aware': False,
            'meta_data': {'value': 'one'},
            'start_time': 3289798798732,
            'used_cache': False,
            'uuid': '89s7df987sdf7'},
            mock_archive.archive_stage_context)

    def test_load_stage_log_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        mock_archive.fetch_stage_uuid = '90s8d'
        stage_context.load_stage_log_from_archive(mock_archive)
        self.assertEqual('90s8d', stage_context.stage_log)

    def test_load_persisted_data_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        mock_archive.fetch_persisted_uuid = '190uh23'
        mock_archive.fetch_model_uuid = '0912h1'
        stage_context.load_persisted_data_from_archive(mock_archive)
        self.assertEqual('190uh23', stage_context.stage_output)
        self.assertEqual('0912h1', stage_context.model_data)

    def test_load_provenance_from_archive_has_complete_mock_attributes(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_provenance_from_archive(mock_archive)

    def test_load_job_source_from_archive_has_complete_mock_attributes(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_job_source_from_archive(mock_archive)

    def test_load_artifact_from_archive_has_complete_mock_attributes(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_artifact_from_archive(mock_archive)

    def test_load_miscellaneous_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_miscellaneous_from_archive(mock_archive)
        self.assertEqual({}, stage_context.meta_data)
        self.assertIsNone(stage_context.data_uuid)
        self.assertIsNone(stage_context.uuid)
        self.assertIsNone(stage_context.error_information)
        self.assertIsNone(stage_context.start_time)
        self.assertIsNone(stage_context.end_time)
        self.assertIsNone(stage_context.delta_time)
        self.assertFalse(stage_context.is_context_aware)
        self.assertFalse(stage_context.used_cache)
        self.assertIsNone(stage_context.cache_uuid)
        self.assertFalse(stage_context.cache_read_time)
        self.assertIsNone(stage_context.cache_write_time)
        self.assertIsNone(stage_context.has_stage_output)

    def test_load_miscellaneous_from_archive_with_specific_values(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.meta_data = {'value': 'one'}
        stage_context.data_uuid = 'sd9f8sdf'
        stage_context.stage_output = 'some output from model'
        stage_context.uuid = '89s7df987sdf7'
        stage_context.error_information = 'an error message'
        stage_context.model_data = 'model data'
        stage_context.start_time = 3289798798732
        stage_context.end_time = 92380982309
        stage_context.delta_time = 398098
        stage_context.is_context_aware = False
        stage_context.used_cache = False
        stage_context.cache_uuid = None
        stage_context.cache_read_time = False
        stage_context.cache_write_time = None
        stage_context.has_stage_output = None

        stage_context.load_miscellaneous_from_archive(mock_archive)

        self.assertEqual({'value': 'one'}, stage_context.meta_data)
        self.assertEqual('sd9f8sdf', stage_context.data_uuid)
        self.assertEqual('some output from model', stage_context.stage_output)
        self.assertEqual('89s7df987sdf7', stage_context.uuid)
        self.assertEqual('an error message', stage_context.error_information)
        self.assertEqual('model data', stage_context.model_data)
        self.assertEqual(3289798798732, stage_context.start_time)
        self.assertEqual(92380982309, stage_context.end_time)
        self.assertEqual(398098, stage_context.delta_time)
        self.assertFalse(stage_context.is_context_aware)
        self.assertFalse(stage_context.used_cache)
        self.assertIsNone(stage_context.cache_uuid)
        self.assertFalse(stage_context.cache_read_time)
        self.assertIsNone(stage_context.cache_write_time)
        self.assertIsNone(stage_context.has_stage_output)

    @patch('time.sleep', return_value=1)
    def mock_sleeping_callback(self, patched_time_sleep, sleep_time):
        import time

        def callback():
            time.sleep(sleep_time)
            return "sleep_time=" + str(sleep_time)

        return callback

    @patch('time.time', return_value=1)
    def test_time_callback_one_second(self, patched_time_sleep):
        import time

        stage_context = StageContext()

        start_time = time.time()
        stage_context.time_callback(self.mock_sleeping_callback(1))
        end_time = time.time()

        self.assertEqual(start_time, stage_context.start_time)
        self.assertEqual(end_time, stage_context.end_time)
        self.assertEqual(0, stage_context.delta_time)
