
import unittest
from mock import patch
from foundations_rest_api.v2beta.models.property_model import PropertyModel

from test.helpers import let
from test.helpers.spec import Spec


class TestJobsControllerV2(Spec):
    class MockProject(PropertyModel):
        name = PropertyModel.define_property()
        jobs = PropertyModel.define_property()
        output_metric_names = PropertyModel.define_property()
        garbage = PropertyModel.define_property()
        parameters = PropertyModel.define_property()

    def _make_lazy_result(self, name, jobs, output_metric_names=None, parameters=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _callback():
            return self.MockProject(
                name=name,
                jobs=jobs,
                output_metric_names=output_metric_names or [],
                parameters=parameters or []
            )

        return LazyResult(_callback)

    @let
    def _project_find_by(self):
        return self.patch("foundations_rest_api.v2beta.models.project.Project.find_by")

    @let
    def _empty_lazy_result(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        return LazyResult(lambda: None)

    @let
    def _controller(self):
        from foundations_rest_api.v2beta.controllers.jobs_controller import (
            JobsController,
        )

        return JobsController()

    def test_index_returns_only_completed_jobs(self):
        self._project_find_by.return_value = self._make_lazy_result(
            "some project",
            jobs=["completed job 1", "running job 2"],
            output_metric_names="metrics",
            parameters=[],
        )

        self._controller.params = {"project_name": "the great potato project"}

        expected_result = {
            "jobs": ["completed job 1", "running job 2"],
            "name": "some project",
            "output_metric_names": "metrics",
            "parameters": [],
        }
        self.assertEqual(expected_result, self._controller.index().as_json())
        self._project_find_by.assert_called_with(name="the great potato project")

    def test_index_returns_only_running_jobs(self):
        self._project_find_by.return_value = self._make_lazy_result(
            "some project",
            jobs=["completed job 1", "running job 2"]
        )

        self._controller.params = {"project_name": "the not so great potato project"}

        expected_result = {
            "jobs": ["completed job 1", "running job 2"],
            "name": "some project",
            "output_metric_names": [],
            "parameters": [],
        }
        self.assertEqual(expected_result, self._controller.index().as_json())
        self._project_find_by.assert_called_with(name="the not so great potato project")

    def test_index_404s_a_missing_project(self):
        self._project_find_by.return_value = self._empty_lazy_result

        self._controller.params = {"project_name": "the not so great potato project"}

        self.assertEqual(404, self._controller.index().status())

    def test_index_returns_an_error_message_for_a_missing_project(self):
        self._project_find_by.return_value = self._empty_lazy_result

        self._controller.params = {"project_name": "the not so great potato project"}

        self.assertEqual(
            "This project was not found", self._controller.index().as_json()
        )
