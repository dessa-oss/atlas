"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.spec import Spec

class TestAnnotate(Spec):

    @let
    def redis(self):
        from fakeredis import FakeRedis
        return FakeRedis()

    @let
    def consumer(self):
        from foundations_contrib.consumers.jobs.queued.annotate import Annotate
        return Annotate(self.redis)

    @let
    def job_id(self):
        from uuid import uuid4
        return uuid4()

    @let
    def annotations(self):
        return {self.faker.name(): self.faker.sentence() for _ in range(self.annotation_count)}

    @let
    def annotation_count(self):
        import random
        return random.randint(2, 10)

    def test_call_saves_annotations(self):
        time = 1551457960.22515
        self.consumer.call({'job_id': self.job_id, 'annotations': self.annotations}, None, None)
        result_annotations = self.redis.hgetall('jobs:{}:annotations'.format(self.job_id))
        decoded_annotations = {key.decode(): value.decode() for key, value in result_annotations.items()}
        self.assertEqual(self.annotations, decoded_annotations)