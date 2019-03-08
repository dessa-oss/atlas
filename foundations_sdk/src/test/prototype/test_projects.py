"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn
from foundations_internal.testing.helpers import *
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from uuid import uuid4

from foundations.prototype.projects import *

class TestPrototypeProjects(Spec):

    @let
    def provenance_annotations(self):
        return {}

    @let_now
    def redis(self):
        from fakeredis import FakeRedis
        return self.patch('foundations_contrib.global_state.redis_connection', FakeRedis())
    
    @let_now
    def get_metrics_mock(self):
        conditional_mock = ConditionalReturn()
        self.patch('foundations.get_metrics_for_all_jobs', conditional_mock)
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
        return DataFrame([
            {
                'loss': '99',
                'job_id': self.job_id,
            }, {
                'loss': '34',
                'job_id': self.job_id_two,
            }
        ])

    @let
    def annotations(self):
        return {
            'model': 'mlp',
            'learning rate': '999999'
        }

    @let
    def annotations_data_frame(self):
        return DataFrame([
            {'tag_{}'.format(key): value for key, value in self.annotations.items()}
        ])

    @let
    def annotations_two(self):
        return {
            'model': 'logreg',
            'learning rate': '5465'
        }

    @let
    def random_tag(self):
        return self.faker.name()

    @let
    def random_tag_value(self):
        return self.faker.sentence()

    @let
    def annotations_data_frame_two(self):
        return DataFrame([
            {'tag_{}'.format(key): value for key, value in self.annotations_two.items()}
        ])

    mock_logger = let_mock()

    @let_now
    def get_logger_mock(self):
        from foundations_internal.testing.helpers.conditional_return import ConditionalReturn

        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.prototype.projects')
        return mock

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import foundations_context

        foundations_context.pipeline_context().provenance.annotations = self.provenance_annotations

    def test_returns_metrics_data_frame(self):
        metrics = get_metrics_for_all_jobs(self.project_name)
        metric_subset = metrics[list(self.metrics)]
        assert_frame_equal(self.metrics, metric_subset)

    def test_returns_stored_annotations(self):
        from foundations_contrib.consumers.jobs.queued.annotate import Annotate
        
        Annotate(self.redis).call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        
        metrics = get_metrics_for_all_jobs(self.project_name)
        job_metrics = metrics[metrics['job_id'] == self.job_id]
        job_annotations = job_metrics[list(self.annotations_data_frame)]

        assert_frame_equal(self.annotations_data_frame, job_annotations)

    def test_returns_stored_annotations_multiple_annotations(self):
        from foundations_contrib.consumers.jobs.queued.annotate import Annotate
        import pandas
        
        annotator = Annotate(self.redis)
        annotator.call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        annotator.call({'job_id': self.job_id_two, 'annotations': self.annotations_two}, None, {})
        
        metrics = get_metrics_for_all_jobs(self.project_name)
        job_annotations = metrics[list(self.annotations_data_frame)]

        expected_data_frame = pandas.concat([self.annotations_data_frame, self.annotations_data_frame_two], ignore_index=True)
        assert_frame_equal(expected_data_frame, job_annotations)

    def test_set_tag_stores_tag_in_provenance(self):
        set_tag(self.random_tag, self.random_tag_value)
        self.assertEqual({self.random_tag: self.random_tag_value}, self.provenance_annotations)

    def test_set_tag_logs_warning_when_set_twice(self):
        set_tag(self.random_tag, self.random_tag_value)
        set_tag(self.random_tag, self.random_tag_value)
        self.mock_logger.warn.assert_called_with('Tag `{}` updated to `{}`'.format(self.random_tag, self.random_tag_value))
        
    def test_get_metrics_for_all_jobs_is_global(self):
        import foundations.prototype
        self.assertEqual(get_metrics_for_all_jobs, foundations.prototype.get_metrics_for_all_jobs)

