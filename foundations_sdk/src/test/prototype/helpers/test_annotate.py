"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn
from foundations_spec.helpers import *
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from uuid import uuid4

from foundations.prototype.helpers.annotate import *

@skip
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
    def annotations(self):
        return self._generate_annotations()

    @let
    def annotations_two(self):
        return self._generate_annotations()

    def test_job_annotations_returns_stored_annotations_for_single_job(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        Annotate(self.redis).call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        self.assertEqual(self.annotations, job_annotations(self.redis, self.job_id))

    def test_annotations_for_multiple_jobs_returns_annotations_for_single_job(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        Annotate(self.redis).call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        self.assertEqual({self.job_id: self.annotations}, annotations_for_multiple_jobs(self.redis, [self.job_id]))

    def test_annotations_for_multiple_jobs_returns_annotations_for_multiple_jobs(self):
        from foundations_contrib.consumers.annotate import Annotate
        
        annotate = Annotate(self.redis)
        annotate.call({'job_id': self.job_id, 'annotations': self.annotations}, None, {})
        annotate.call({'job_id': self.job_id_two, 'annotations': self.annotations_two}, None, {})

        result_annotations = annotations_for_multiple_jobs(self.redis, [self.job_id, self.job_id_two])
        expected_annotations = {self.job_id: self.annotations, self.job_id_two: self.annotations_two}

        self.assertEqual(expected_annotations, result_annotations)

    def _generate_annotations(self):
        import random
        
        annotation_count = random.randint(2, 10)
        return {self.faker.name(): self.faker.sentence() for _ in range(annotation_count)}
