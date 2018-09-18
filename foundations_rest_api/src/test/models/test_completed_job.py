"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.models.completed_job import CompletedJob


class TestCompletedJob(unittest.TestCase):

    class MockArchiveListing(object):

        def __init__(self):
            pass

        def get_pipeline_names(self):
            return self._list

        def set_listing(self, listing):
            self._list = listing

    def setUp(self):
        from foundations.global_state import config_manager

        config_manager['archive_listing_implementation'] = {
            'archive_listing_type': self.MockArchiveListing
        }

    def tearDown(self):
        from foundations.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = CompletedJob(job_id=job_id)
        
        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = CompletedJob(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = CompletedJob(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_input_params(self):
        job = CompletedJob(input_params={'a': 5})
        self.assertEqual({'a': 5}, job.input_params)
        
    def test_has_input_params_different_params(self):
        job = CompletedJob(input_params={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.input_params)

    def test_has_output_metrics(self):
        job = CompletedJob(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)
        
    def test_has_output_metrics_different_params(self):
        job = CompletedJob(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)
        
    def test_has_status(self):
        job = CompletedJob(status='completed')
        self.assertEqual('completed', job.status)
        
    def test_has_status_different_params(self):
        job = CompletedJob(status='completed in error')
        self.assertEqual('completed in error', job.status)
        