"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v2beta.models.project import Project
from foundations_rest_api.v2beta.models.property_model import PropertyModel
from test.helpers.mock_mixin import MockMixin

class TestProjectV2(MockMixin, unittest.TestCase):

    class MockListing(object):

        def __init__(self):
            self.list = []

        def get_pipeline_names(self):
            return self.list
        
    class MockJob(PropertyModel):
        job_id = PropertyModel.define_property()
        input_params = PropertyModel.define_property()
        output_metrics = PropertyModel.define_property()

    def setUp(self):
        super(TestProjectV2, self).setUp()
        self._find_project = self.patch('foundations_contrib.models.project_listing.ProjectListing.find_project')

    def tearDown(self):
        from foundations.global_state import config_manager

        super(TestProjectV2, self).tearDown()

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

    def test_find_looks_for_correct_project(self):
        from foundations.global_state import redis_connection

        Project.find_by(name='my favourite project').evaluate()
        self._find_project.assert_called_with(redis_connection, 'my favourite project')

    def test_find_looks_for_correct_project_different_project(self):
        from foundations.global_state import redis_connection

        Project.find_by(name='my least favourite project').evaluate()
        self._find_project.assert_called_with(redis_connection, 'my least favourite project')

    def test_find_returns_none_when_project_does_not_exist(self):
        self._find_project.return_value = None
        project = Project.find_by(name='my least favourite project').evaluate()
        self.assertIsNone(project)

    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id = '123', input_params= [], output_metrics = [])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [],
            output_metric_names = []
        )
        self.assertEqual(expected_project, project)
    

    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects_multiple_projects(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id = '123', input_params= [], output_metrics = [])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}, {'name': 'project2'}]

        project = [project for project in Project.all().evaluate()]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [],
            output_metric_names = []
        )
        expected_project_two = Project(
            name='project2',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [],
            output_metric_names = []
        )
        self.assertEqual([expected_project, expected_project_two], project)
    
    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_correct_input_param_names(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id='123',
                                                                  input_params=[{'name': 'param_1', 'value': 'bye', 'type': 'string'}],
                                                                  output_metrics=[])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [{'name': 'param_1', 'type': 'string'}],
            output_metric_names = []
        )
        self.assertDictEqual(expected_project.input_parameter_names[0], project.input_parameter_names[0])
    
    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_correct_input_param_names_2_input_param(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id='123',
                                                                  input_params=[{'name': 'param_1', 'value': 'bye', 'type': 'string'},
                                                                                {'name': 'param_2', 'value': '[hi]', 'type': 'list'}],
                                                                  output_metrics=[])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [{'name': 'param_1', 'type': 'string'}, {'name': 'param_2', 'type': 'list'}],
            output_metric_names = []
        )
        self.assertCountEqual(expected_project.input_parameter_names, project.input_parameter_names)
    
    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_correct_ouput_metric_names(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id='123',
                                                                  input_params=[],
                                                                  output_metrics=[{'name': 'metric_1', 'type': 'list'}])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [],
            output_metric_names = [{'name': 'metric_1', 'type': 'list'}]
        )
        self.assertCountEqual(expected_project.output_metric_names, project.output_metric_names)
    
    @patch('foundations_rest_api.v2beta.models.job.Job.all')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_correct_ouput_metric_names_multiple_metrics(self, mock_projects, mock_jobs):
        from foundations_rest_api.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(lambda: [self.MockJob(job_id='123',
                                                                  input_params=[],
                                                                  output_metrics=[{'name': 'metric_1', 'type': 'list'},
                                                                                {'name': 'metric_2', 'type': 'string'},
                                                                                {'name': 'metric_3', 'type': 'hippo'}])])

        mock_projects.list_projects.return_value = [{'name': 'project1'}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name='project1',
            created_at = None,
            owner = None,
            jobs = [self.MockJob(job_id = '123', input_params= [], output_metrics = [])],
            input_parameter_names = [],
            output_metric_names=[{'name': 'metric_1', 'type': 'list'},
                                 {'name': 'metric_2', 'type': 'string'},
                                 {'name': 'metric_3', 'type': 'hippo'}
                                 ]
        )
        self.assertCountEqual(expected_project.output_metric_names, project.output_metric_names)


    @patch('foundations.global_state.redis_connection')
    @patch('foundations_contrib.models.project_listing.ProjectListing')
    def test_all_returns_all_projects_using_correct_redis(self, mock_projects, mock_redis):
        Project.all().evaluate()
        mock_projects.list_projects.assert_called_with(mock_redis)  
