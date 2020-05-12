
import unittest
from mock import patch

from foundations.projects import *
from foundations_spec.helpers import *
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from uuid import uuid4
from foundations import set_tag


class TestProjects(Spec):
    foundations_context = let_patch_instance(
        "foundations_contrib.global_state.current_foundations_context"
    )
    message_router = let_patch_mock("foundations_contrib.global_state.message_router")

    @let
    def provenance_annotations(self):
        return {}

    @let
    def random_boolean(self):
        return self.faker.boolean()

    @let_now
    def redis(self):
        from fakeredis import FakeRedis

        return self.patch(
            "foundations_contrib.global_state.redis_connection", FakeRedis()
        )

    @let
    def get_metrics_mock(self):
        conditional_mock = ConditionalReturn()
        self.patch("foundations.projects._get_metrics_for_all_jobs", conditional_mock)
        conditional_mock.return_when(self.metrics, self.project_name)

        return conditional_mock

    @let
    def project_name(self):
        return self.faker.name()

    @let
    def job_id(self):
        return self.faker.sha256()

    @let
    def job_id_two(self):
        return self.faker.sha256()

    @let
    def metrics(self):
        return DataFrame(
            [
                {"loss": "99", "job_id": self.job_id,},
                {"loss": "34", "job_id": self.job_id_two,},
            ]
        )

    @let
    def annotations(self):
        return {"model": "mlp", "learning rate": "999999"}

    @let
    def annotations_data_frame(self):
        return DataFrame(
            [{"tag_{}".format(key): value for key, value in self.annotations.items()}]
        )

    @let
    def annotations_two(self):
        return {"model": "logreg", "learning rate": "5465"}

    @let
    def random_tag(self):
        return self.faker.name()

    @let
    def random_tag_value(self):
        return self.faker.sentence()

    @let
    def annotations_data_frame_two(self):
        return DataFrame(
            [
                {
                    "tag_{}".format(key): value
                    for key, value in self.annotations_two.items()
                }
            ]
        )

    mock_logger = let_mock()

    @let_now
    def get_logger_mock(self):
        from foundations_spec.helpers.conditional_return import ConditionalReturn

        mock = self.patch(
            "foundations_contrib.log_manager.LogManager.get_logger", ConditionalReturn()
        )
        mock.return_when(Mock(), "foundations_events.consumers.annotate")
        mock.return_when(self.mock_logger, "foundations.utils")
        return mock

    @set_up
    def set_up(self):
        self.foundations_context.job_id = None
        self.foundations_context.project_name = self.project_name

        self.foundations_context.provenance.annotations = (
            self.provenance_annotations
        )
        self.redis.flushall()

    def test_set_project_name_sets_project_name(self):
        set_project_name(self.project_name)
        self.assertEqual(
            self.project_name,
            self.foundations_context.project_name,
        )

    def test_set_project_name_sets_project_name_different_name(self):
        set_project_name(self.project_name)
        self.assertEqual(
            self.project_name,
            self.foundations_context.project_name,
        )

    def test_set_project_name_is_global(self):
        import foundations

        foundations.set_project_name(self.project_name)
        self.assertEqual(
            self.project_name,
            self.foundations_context.project_name,
        )

    def test_set_project_name_is_global(self):
        import foundations

        foundations.set_project_name(self.project_name)
        self.assertEqual(
            self.project_name,
            self.foundations_context.project_name,
        )

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data(
        self, listing_mock, find_mock
    ):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        output_metrics = {"loss": 100}
        listing_mock.return_value = [
            {
                "project_name": self.project_name,
                "job_parameters": {"a": 5},
                "output_metrics": output_metrics,
            }
        ]

        expected_result = DataFrame(
            [
                {
                    "project_name": self.project_name,
                    "loss": 100,
                    "a": 5,
                }
            ]
        )
        assert_frame_equal(
            expected_result,
            get_metrics_for_all_jobs(self.project_name),
            check_like=True,
        )

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_without_input_parameters(
        self, listing_mock, find_mock
    ):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        output_metrics = {"loss": 100}
        listing_mock.return_value = [
            {
                "project_name": self.project_name,
                "job_parameters": {"a": 5},
                "output_metrics": output_metrics,
            }
        ]

        expected_result = DataFrame(
            [{"project_name": self.project_name, "loss": 100, "a": 5}]
        )
        assert_frame_equal(
            expected_result,
            get_metrics_for_all_jobs(self.project_name),
            check_like=True,
        )

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_with_two_variables_same_name_different_position_in_list(
        self, listing_mock, find_mock
    ):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        output_metrics = {"loss": 100}
        listing_mock.return_value = [
            {
                "project_name": self.project_name,
                "job_parameters": {"a": 5},
                "output_metrics": output_metrics,
            }
        ]

        expected_result = DataFrame(
            [
                {
                    "project_name": self.project_name,
                    "loss": 100,
                    "a": 5,
                }
            ]
        )
        assert_frame_equal(
            expected_result,
            get_metrics_for_all_jobs(self.project_name),
            check_like=True,
        )

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_different_data(
        self, listing_mock, find_mock
    ):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        output_metrics = {"loss": 100}

        output_metrics_2 = {"win": 56}
        listing_mock.return_value = [
            {
                "project_name": "project2",
                "job_parameters": {"a": 5},
                "output_metrics": output_metrics,
            },
            {
                "project_name": "project2",
                "job_parameters": {"bad": 77},
                "output_metrics": output_metrics_2,
            },
        ]

        expected_data = [
            {
                "project_name": "project2",
                "loss": 100,
                "a": 5,
                "bad": None,
            },
            {
                "project_name": "project2",
                "win": 56,
                "a": None,
                "bad": 77,
            },
        ]
        expected_result = DataFrame(expected_data)
        assert_frame_equal(
            expected_result, get_metrics_for_all_jobs("project2"), check_like=True
        )

    @skip
    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_correct_order(self, listing_mock, find_mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        output_metrics = {"loss": 100}

        listing_mock.return_value = [
            {
                "job_id": "aksjhdkajsdh",
                "project_name": self.project_name,
                "job_parameters": {"a": 5},
                "output_metrics": output_metrics,
            }
        ]

        expected_data = [
            {
                "job_id": "aksjhdkajsdh",
                "project_name": self.project_name,
                "b-0": "1",
                "c-1": "2",
                "d-2": "3",
                "loss": 100,
                "a": 5,
            },
        ]
        expected_result = DataFrame(
            expected_data,
            columns=["job_id", "project_name", "a", "b-0", "c-1", "d-2", "loss"],
        )

        assert_frame_equal(expected_result, get_metrics_for_all_jobs(self.project_name))

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_missing_project(self, listing_mock, find_mock):
        find_mock.return_value = None

        with self.assertRaises(ValueError) as error_context:
            get_metrics_for_all_jobs(self.project_name)

        error_string = "Project `{}` does not exist!".format(self.project_name)
        self.assertTrue(error_string in error_context.exception.args)

    @patch("foundations_contrib.models.project_listing.ProjectListing.find_project")
    @patch(
        "foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data"
    )
    def test_get_metrics_for_all_jobs_missing_project_different_project(
        self, listing_mock, find_mock
    ):
        find_mock.return_value = None

        with self.assertRaises(ValueError) as error_context:
            get_metrics_for_all_jobs("project numba 5")

        self.assertTrue(
            "Project `project numba 5` does not exist!" in error_context.exception.args
        )

    def test_get_metrics_for_all_jobs_is_defined_globally(self):
        import foundations

        self.assertEqual(get_metrics_for_all_jobs, foundations.get_metrics_for_all_jobs)

    def test_returns_metrics_data_frame(self):
        self.get_metrics_mock
        metrics = get_metrics_for_all_jobs(self.project_name)
        metric_subset = metrics[list(self.metrics)]
        assert_frame_equal(self.metrics, metric_subset)

    def test_returns_stored_annotations(self):
        from foundations_events.consumers.annotate import Annotate

        self.get_metrics_mock

        annotator = Annotate(self.redis)

        self._annotate_jobs(annotator, self.annotations, self.job_id)

        metrics = get_metrics_for_all_jobs(self.project_name)
        job_metrics = metrics[metrics["job_id"] == self.job_id]
        job_annotations = job_metrics[list(self.annotations_data_frame)]

        assert_frame_equal(self.annotations_data_frame, job_annotations)

    def test_returns_stored_annotations_multiple_annotations(self):
        from foundations_events.consumers.annotate import Annotate
        import pandas

        self.get_metrics_mock
        annotator = Annotate(self.redis)

        self._annotate_jobs(annotator, self.annotations, self.job_id)
        self._annotate_jobs(annotator, self.annotations_two, self.job_id_two)

        metrics = get_metrics_for_all_jobs(self.project_name)
        job_annotations = metrics[list(self.annotations_data_frame)]

        expected_data_frame = pandas.concat(
            [self.annotations_data_frame, self.annotations_data_frame_two],
            ignore_index=True,
        )
        assert_frame_equal(expected_data_frame, job_annotations)

    def test_set_tag_when_in_job_sets_tag(self):
        self.foundations_context.job_id = self.job_id
        set_tag(self.random_tag, self.random_tag_value)
        self.message_router.push_message.assert_called_with(
            "job_tag",
            {
                "job_id": self.job_id,
                "key": self.random_tag,
                "value": self.random_tag_value,
            },
        )

    def test_get_metrics_for_all_jobs_is_global(self):
        import foundations.projects

        self.assertEqual(
            get_metrics_for_all_jobs, foundations.projects.get_metrics_for_all_jobs
        )

    def _annotate_jobs(self, annotator, annotations, job_id):
        for key, value in annotations.items():
            annotator.call({"job_id": job_id, "key": key, "value": value}, None, {})
