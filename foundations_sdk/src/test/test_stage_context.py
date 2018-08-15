"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.stage_context import StageContext


class TestStageContext(unittest.TestCase):

    class MockArchive(object):

        def __init__(self):
            self.archive_provenance = None

        def append_stage_log(self, uuid, stage_log):
            pass

        def append_stage_persisted_data(self, uuid, stage_output):
            pass

        def append_stage_model_data(self, uuid, model_data):
            pass

        def append_stage_miscellaneous(self, uuid, stage_context, archive_stage_context):
            pass

        def fetch_stage_log(self, uuid):
            return '90s8d'

        def fetch_stage_persisted_data(self, stage_uuid_string):
            return '190uh23'

        def fetch_stage_model_data(self, stage_uuid_string):
            return '0912h1'

    def test_set_stage_output(self):
        stage_context = StageContext()
        stage_context.set_stage_output('some stage output')
        self.assertEqual('some stage output', stage_context.stage_output)

    def test_set_stage_output_has_stage_after_run(self):
        stage_context = StageContext()
        self.assertEqual(None, stage_context.has_stage_output)
        stage_context.set_stage_output('some stage output')
        self.assertTrue(stage_context.has_stage_output)

    def test_add_error_information(self):
        import sys
        stage_context = StageContext()

        mock_exception = sys.exc_info()
        stage_context.add_error_information(mock_exception)
        self.assertEqual({'type': None, 'exception': None,
                          'traceback': []}, stage_context.error_information)

    def test_save_to_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.save_to_archive(mock_archive)

    def test_load_stage_log_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_stage_log_from_archive(mock_archive)
        self.assertEqual('90s8d', stage_context.stage_log)

    def test_load_persisted_data_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_persisted_data_from_archive(mock_archive)
        self.assertEqual('190uh23', stage_context.stage_output)
        self.assertEqual('0912h1', stage_context.model_data)

    def test_load_provenance_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_provenance_from_archive(mock_archive)

    def test_load_job_source_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_job_source_from_archive(mock_archive)

    def test_load_artifact_from_archive(self):
        stage_context = StageContext()
        mock_archive = self.MockArchive()

        stage_context.load_artifact_from_archive(mock_archive)
