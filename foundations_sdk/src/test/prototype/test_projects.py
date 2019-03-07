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
        from pandas import DataFrame

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
            'learning rate': 999999
        }

    @let
    def annotations_two(self):
        return {
            'model': 'logreg',
            'learning rate': 5465
        }

    def test_returns_metrics_data_frame(self):
        metrics = get_metrics_for_all_jobs(self.project_name)
        metric_subset = metrics[list(self.metrics)]
        assert_frame_equal(self.metrics, metric_subset)

    @skip
    def test_returns_stored_annotations(self):
        from foundations_contrib.consumers.jobs.queued.annotate import Annotate
        
        annotator = Annotate(self.redis)
        annotator.call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        annotator.call({'job_id': self.job_id_two, 'annotations': self.annotations_two}, None, {})
