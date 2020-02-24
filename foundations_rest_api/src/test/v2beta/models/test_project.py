

import unittest
from mock import patch
from foundations_rest_api.v2beta.models.project import Project
from foundations_rest_api.v2beta.models.property_model import PropertyModel
from foundations_spec import *


class TestProjectV2(Spec):
    class MockListing(object):
        def __init__(self):
            self.list = []

        def get_pipeline_names(self):
            return self.list

    class MockJob(PropertyModel):
        job_id = PropertyModel.define_property()
        output_metrics = PropertyModel.define_property()
        job_parameters = PropertyModel.define_property()

    @set_up
    def project_set_up(self):
        import fakeredis

        self._find_project = self.patch(
            "foundations_contrib.models.project_listing.ProjectListing.find_project"
        )
        self._redis = self.patch(
            "foundations_rest_api.global_state.redis_connection", fakeredis.FakeRedis()
        )

    def test_new_project_is_response(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        lazy_result = Project.new(name="my first project")
        self.assertTrue(isinstance(lazy_result, LazyResult))

    def test_new_project_is_response_containing_project(self):
        lazy_result = Project.new(name="my first project")
        self.assertTrue(isinstance(lazy_result.evaluate(), Project))

    def test_new_project_has_name(self):
        lazy_result = Project.new(name="my first project")
        self.assertEqual("my first project", lazy_result.evaluate().name)

    def test_new_project_has_name_different_name(self):
        lazy_result = Project.new(name="my favourite project")
        self.assertEqual("my favourite project", lazy_result.evaluate().name)

    def test_find_by_name_project_is_response(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        lazy_result = Project.find_by(name="my first project")
        self.assertTrue(isinstance(lazy_result, LazyResult))

    @quarantine
    def test_find_by_name_project_is_response_containing_project(self):
        lazy_result = Project.find_by(name="my first project")
        self.assertTrue(isinstance(lazy_result.evaluate(), Project))

    def test_find_by_name_project_has_name(self):
        lazy_result = Project.find_by(name="my first project")
        self.assertEqual("my first project", lazy_result.evaluate().name)

    @quarantine
    def test_find_by_name_project_has_name_different_name(self):
        lazy_result = Project.find_by(name="my favourite project")
        self.assertEqual("my favourite project", lazy_result.evaluate().name)

    def test_find_looks_for_correct_project(self):
        Project.find_by(name="my favourite project").evaluate()
        self._find_project.assert_called_with(self._redis, "my favourite project")

    def test_find_looks_for_correct_project_different_project(self):
        Project.find_by(name="my least favourite project").evaluate()
        self._find_project.assert_called_with(self._redis, "my least favourite project")

    def test_find_returns_none_when_project_does_not_exist(self):
        self._find_project.return_value = None
        project = Project.find_by(name="my least favourite project").evaluate()
        self.assertIsNone(project)

    @patch("foundations_rest_api.v2beta.models.job.Job.all")
    @patch("foundations_contrib.models.project_listing.ProjectListing")
    def test_all_returns_all_projects(self, mock_projects, mock_jobs):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(
            lambda: [self.MockJob(job_id="123", job_parameters=[], output_metrics=[])]
        )

        mock_projects.list_projects.return_value = [{"name": "project1"}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name="project1",
            created_at=None,
            owner=None,
            jobs=[self.MockJob(job_id="123", job_parameters=[], output_metrics=[])],
            output_metric_names=[],
            parameters=[]
        )
        self.assertEqual(expected_project, project)

    @patch("foundations_rest_api.v2beta.models.job.Job.all")
    @patch("foundations_contrib.models.project_listing.ProjectListing")
    def test_all_returns_all_projects_multiple_projects(self, mock_projects, mock_jobs):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(
            lambda: [self.MockJob(job_id="123", job_parameters=[], output_metrics=[])]
        )

        mock_projects.list_projects.return_value = [
            {"name": "project1"},
            {"name": "project2"},
        ]

        projects = [project for project in Project.all().evaluate()]

        expected_project = Project(
            name="project1",
            created_at=None,
            owner=None,
            jobs=[self.MockJob(job_id="123", job_parameters=[], output_metrics=[])],
            output_metric_names=[],
            parameters=[]
        )
        expected_project_two = Project(
            name="project2",
            created_at=None,
            owner=None,
            jobs=[self.MockJob(job_id="123", job_parameters=[], output_metrics=[])],
            output_metric_names=[],
            parameters=[]
        )
        self.assertEqual([expected_project, expected_project_two], projects)

    @patch("foundations_rest_api.v2beta.models.job.Job.all")
    @patch("foundations_contrib.models.project_listing.ProjectListing")
    def test_all_returns_correct_output_metric_names(self, mock_projects, mock_jobs):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(
            lambda: [
                self.MockJob(
                    job_id="123",
                    job_parameters=[],
                    output_metrics=[{"name": "metric_1", "type": "list"}],
                )
            ]
        )

        mock_projects.list_projects.return_value = [{"name": "project1"}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name="project1",
            created_at=None,
            owner=None,
            jobs=[self.MockJob(job_id="123", job_parameters=[], output_metrics=[])],
            output_metric_names=[{"name": "metric_1", "type": "list"}],
            parameters=[]
        )
        self.assertCountEqual(
            expected_project.output_metric_names, project.output_metric_names
        )

    @patch("foundations_rest_api.v2beta.models.job.Job.all")
    @patch("foundations_contrib.models.project_listing.ProjectListing")
    def test_all_returns_correct_output_metric_names_multiple_metrics(
        self, mock_projects, mock_jobs
    ):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        mock_jobs.return_value = LazyResult(
            lambda: [
                self.MockJob(
                    job_id="123",
                    job_parameters=[],
                    output_metrics=[
                        {"name": "metric_1", "type": "list"},
                        {"name": "metric_2", "type": "string"},
                        {"name": "metric_3", "type": "hippo"},
                    ],
                )
            ]
        )

        mock_projects.list_projects.return_value = [{"name": "project1"}]

        project = Project.all().evaluate()[0]
        expected_project = Project(
            name="project1",
            created_at=None,
            owner=None,
            jobs=[self.MockJob(job_id="123", job_parameters=[], output_metrics=[])],
            output_metric_names=[
                {"name": "metric_1", "type": "list"},
                {"name": "metric_2", "type": "string"},
                {"name": "metric_3", "type": "hippo"},
            ],
        )
        self.assertCountEqual(
            expected_project.output_metric_names, project.output_metric_names
        )

    @patch("foundations_rest_api.global_state.redis_connection")
    @patch("foundations_contrib.models.project_listing.ProjectListing")
    def test_all_returns_all_projects_using_correct_redis(
        self, mock_projects, mock_redis
    ):
        Project.all().evaluate()
        mock_projects.list_projects.assert_called_with(mock_redis)
