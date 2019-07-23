"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from foundations.helpers.annotate import *

class TestAnnotate(Spec):
    
    @let_now
    def redis(self):
        from fakeredis import FakeRedis
        return FakeRedis()

    @let
    def job_id(self):
        return self.faker.sha256()

    @let
    def job_id_two(self):
        return self.faker.sha256()

    @let
    def key(self):
        return self.faker.word()

    @let
    def key_two(self):
        return self.faker.word()

    @let
    def value(self):
        return self.faker.sentence()

    @let
    def value_two(self):
        return self.faker.sentence()

    def test_job_annotations_returns_stored_annotations_for_single_job(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        Annotate(self.redis).call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, {})
        self.assertEqual({self.key: self.value}, job_annotations(self.redis, self.job_id))

    def test_annotations_for_multiple_jobs_returns_annotations_for_single_job(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        Annotate(self.redis).call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, {})
        self.assertEqual({self.job_id: {self.key: self.value}}, annotations_for_multiple_jobs(self.redis, [self.job_id]))

    def test_annotations_for_multiple_jobs_returns_annotations_for_multiple_jobs(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        annotate = Annotate(self.redis)
        annotate.call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, {})
        annotate.call({'job_id': self.job_id_two, 'key': self.key_two, 'value': self.value_two}, None, {})

        result_annotations = annotations_for_multiple_jobs(self.redis, [self.job_id, self.job_id_two])
        expected_annotations = {self.job_id: {self.key: self.value}, self.job_id_two: {self.key_two: self.value_two}}

        self.assertEqual(expected_annotations, result_annotations)
