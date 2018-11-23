"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations.job_data_shaper import JobDataShaper


class TestJobDataShaper(unittest.TestCase):

    def test_data_reshaped_one_job(self):
        sample_data = [{
            'project_name': 'banana',
            'job_id': '132',
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'ron': 'weasley'}],
            'output_metrics': [['123', 'hermione', 'granger']],
            'status': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }]
        expected_data = [{
            'project_name': 'banana',
            'job_id': '132',
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'ron': 'weasley'}],
            'output_metrics': {'hermione': 'granger'},
            'status': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))

    def test_data_reshaped_one_job_different_data(self):
        sample_data = [{
            'job_parameters': {'harry': 'potter', 'tom': 'riddle'},
            'input_params': [{'ron': 'weasley'}, {'dudley': 'dursley'}],
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'luna', 'lovegood']],
        }]
        expected_data = [{
            'job_parameters': {'harry': 'potter', 'tom': 'riddle'},
            'input_params': [{'ron': 'weasley'}, {'dudley': 'dursley'}],
            'output_metrics': {'hermione': 'granger', 'luna': 'lovegood'},

        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))

    def test_data_reshaped_two_jobs_different_data(self):
        sample_data = [{
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'luna', 'lovegood']],
        },
            {
            'output_metrics': [['123', 'hermione', 'granger'], ['1245', 'moon', 'lovegood']],
        }]
        expected_data = [{
            'output_metrics': {'hermione': 'granger', 'luna': 'lovegood'},

        },
            {
            'output_metrics': {'hermione': 'granger', 'moon': 'lovegood'},

        }]
        self.assertEqual(expected_data, JobDataShaper.shape_data(sample_data))
