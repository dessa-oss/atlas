"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v2beta.models.project import Project


class TestProjectV2(unittest.TestCase):

    class MockListing(object):

        def __init__(self):
            self.list = []

        def get_pipeline_names(self):
            return self.list

    def setUp(self):
        from foundations.global_state import config_manager

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
        from foundations_rest_api.lazy_result import LazyResult

        lazy_result = Project.new(name='my first project')
        self.assertTrue(isinstance(lazy_result, LazyResult))

    def test_new_project_is_response_containing_project(self):
        lazy_result = Project.new(name='my first project')
        self.assertTrue(isinstance(lazy_result.evaluate(), Project))

    def test_new_project_has_name(self):
        lazy_result = Project.new(name='my first project')
        self.assertEqual('my first project', lazy_result.evaluate().name)

    def test_new_project_has_name_different_name(self):
        lazy_result = Project.new(name='my favourite project')
        self.assertEqual('my favourite project', lazy_result.evaluate().name)

    def test_find_by_name_project_is_response(self):
        from foundations_rest_api.lazy_result import LazyResult

        lazy_result = Project.find_by(name='my first project')
        self.assertTrue(isinstance(lazy_result, LazyResult))

    def test_find_by_name_project_is_response_containing_project(self):
        lazy_result = Project.find_by(name='my first project')
        self.assertTrue(isinstance(lazy_result.evaluate(), Project))

    def test_find_by_name_project_has_name(self):
        lazy_result = Project.find_by(name='my first project')
        self.assertEqual('my first project', lazy_result.evaluate().name)

    def test_find_by_name_project_has_name_different_name(self):
        lazy_result = Project.find_by(name='my favourite project')
        self.assertEqual('my favourite project', lazy_result.evaluate().name)

    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    def test_all_returns_all_projects(self, mock_jobs):
        mock_jobs.return_value = 'listed'

        self._listing.list = ['project1']

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = 'listed'
        )
        self.assertEqual(expected_project, project)

    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    def test_all_returns_all_projects_multiple_projects(self, mock_jobs):
        mock_jobs.return_value = 'listed'

        self._listing.list = ['project1', 'project2']

        project = [project for project in Project.all().evaluate()]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = 'listed'
        )
        expected_project_two = Project(
            name='project2',
            created_at = None,
            owner = None,
            jobs = 'listed'
        )
        self.assertEqual([expected_project, expected_project_two], project)
