"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.models.project import Project


class TestProject(unittest.TestCase):

    class MockListing(object):

        def __init__(self):
            self.list = []

        def get_pipeline_names(self):
            return self.list

    def setUp(self):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext
        from foundations.global_state import config_manager
        from foundations.bucket_pipeline_archive import BucketPipelineArchive

        self._listing = self.MockListing()

        def get_listing():
            return self._listing

        config_manager['project_listing_implementation'] = {
            'project_listing_type': get_listing
        }

    def tearDown(self):
        from foundations.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def test_new_project_is_response(self):
        from foundations_rest_api.response import Response

        response = Project.new(name='my first project')
        self.assertTrue(isinstance(response, Response))

    def test_new_project_is_response_containing_project(self):
        response = Project.new(name='my first project')
        self.assertTrue(isinstance(response.evaluate(), Project))

    def test_new_project_has_name(self):
        response = Project.new(name='my first project')
        self.assertEqual('my first project', response.evaluate().name)

    def test_new_project_has_name_different_name(self):
        response = Project.new(name='my favourite project')
        self.assertEqual('my favourite project', response.evaluate().name)

    def test_find_by_name_project_is_response(self):
        from foundations_rest_api.response import Response

        response = Project.find_by(name='my first project')
        self.assertTrue(isinstance(response, Response))

    def test_find_by_name_project_is_response_containing_project(self):
        response = Project.find_by(name='my first project')
        self.assertTrue(isinstance(response.evaluate(), Project))

    def test_find_by_name_project_has_name(self):
        response = Project.find_by(name='my first project')
        self.assertEqual('my first project', response.evaluate().name)

    def test_find_by_name_project_has_name_different_name(self):
        response = Project.find_by(name='my favourite project')
        self.assertEqual('my favourite project', response.evaluate().name)

    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all')
    def test_find_by_name_project_has_completed_jobs(self, mock):
        mock.return_value = 'some completed jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some completed jobs',
                         response.evaluate().completed_jobs)
        mock.assert_called_with(project_name='my favourite project')

    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all')
    def test_find_by_name_project_has_completed_jobs_different_result(self, mock):
        mock.return_value = 'some other completed jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some other completed jobs',
                         response.evaluate().completed_jobs)
        mock.assert_called_with(project_name='my favourite project')

    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all')
    def test_find_by_name_project_has_completed_jobs_different_name(self, mock):
        mock.return_value = 'some other completed jobs'

        response = Project.find_by(name='my other favourite project')
        self.assertEqual('some other completed jobs',
                         response.evaluate().completed_jobs)
        mock.assert_called_with(project_name='my other favourite project')

    @patch('foundations_rest_api.v1.models.running_job.RunningJob.all')
    def test_find_by_name_project_has_running_jobs(self, mock):
        mock.return_value = 'some running jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some running jobs', response.evaluate().running_jobs)

    @patch('foundations_rest_api.v1.models.running_job.RunningJob.all')
    def test_find_by_name_project_has_running_jobs_different_result(self, mock):
        mock.return_value = 'some other running jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some other running jobs',
                         response.evaluate().running_jobs)

    @patch('foundations_rest_api.v1.models.queued_job.QueuedJob.all')
    def test_find_by_name_project_has_queued_jobs(self, mock):
        mock.return_value = 'some queued jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some queued jobs', response.evaluate().queued_jobs)

    @patch('foundations_rest_api.v1.models.queued_job.QueuedJob.all')
    def test_find_by_name_project_has_queued_jobs_different_result(self, mock):
        mock.return_value = 'some other queued jobs'

        response = Project.find_by(name='my favourite project')
        self.assertEqual('some other queued jobs',
                         response.evaluate().queued_jobs)

    @patch('foundations_rest_api.v1.models.queued_job.QueuedJob.all')
    @patch('foundations_rest_api.v1.models.running_job.RunningJob.all')
    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all')
    def test_all_returns_all_projects(self, mock_completed, mock_running, mock_queued):
        mock_completed.return_value = 'completed'
        mock_running.return_value = 'running'
        mock_queued.return_value = 'queued'

        self._listing.list = ['project1']

        project = Project.all().evaluate()[0].evaluate()
        expected_project = Project(
            name='project1',
            completed_jobs='completed',
            running_jobs='running',
            queued_jobs='queued'
        )
        self.assertEqual(expected_project, project)

    @patch('foundations_rest_api.v1.models.queued_job.QueuedJob.all')
    @patch('foundations_rest_api.v1.models.running_job.RunningJob.all')
    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all')
    def test_all_returns_all_projects_multiple_projects(self, mock_completed, mock_running, mock_queued):
        mock_completed.return_value = 'completed'
        mock_running.return_value = 'running'
        mock_queued.return_value = 'queued'

        self._listing.list = ['project1', 'project2']

        project = [project.evaluate() for project in Project.all().evaluate()]
        expected_project = Project(
            name='project1',
            completed_jobs='completed',
            running_jobs='running',
            queued_jobs='queued'
        )
        expected_project_two = Project(
            name='project2',
            completed_jobs='completed',
            running_jobs='running',
            queued_jobs='queued'
        )
        self.assertEqual([expected_project, expected_project_two], project)
