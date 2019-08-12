"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch, Mock
from foundations_core_rest_api_components.v1.models.project import Project


class TestProject(unittest.TestCase):

    class MockListing(object):

        def __init__(self):
            self.list = []

        def get_pipeline_names(self):
            return self.list

    def tearDown(self):
        from foundations_contrib.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def test_new_project_is_response(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult

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
        from foundations_core_rest_api_components.lazy_result import LazyResult

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

    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects(self, mock_projects):

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None
        )
        self.assertEqual(expected_project, project)

    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects_multiple_projects(self, mock_projects):

        mock_projects.list_projects.return_value = [{'name': 'project1'}, {'name': 'project2'}]

        project = [project for project in Project.all().evaluate()]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None
        )
        expected_project_two = Project(
            name='project2',
            created_at = None,
            owner = None
        )
        self.assertEqual([expected_project, expected_project_two], project)

    @patch('foundations_contrib.global_state.redis_connection')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects_using_correct_redis(self, mock_projects, mock_redis):
        Project.all().evaluate()
        mock_projects.list_projects.assert_called_with(mock_redis)