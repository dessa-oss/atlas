"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers import *
from foundations_spec.helpers.spec import Spec

class TestAnnotate(Spec):

    @let
    def redis(self):
        from fakeredis import FakeRedis
        return FakeRedis()

    @let
    def consumer(self):
        from foundations_contrib.consumers.annotate import Annotate
        self.redis.flushall()
        return Annotate(self.redis)

    @let
    def job_id(self):
        from uuid import uuid4
        return str(uuid4())

    @let
    def key(self):
        return self.faker.word()

    @let
    def value(self):
        return self.faker.sentence()

    @let
    def key_two(self):
        return self.faker.word()

    @let
    def value_two(self):
        return self.faker.sentence()

    def test_call_with_key_value_pair_gets_saved_to_redis(self):
        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, None)
        result_annotations = self.redis.hgetall('jobs:{}:annotations'.format(self.job_id))
        decoded_annotations = {key.decode(): value.decode() for key, value in result_annotations.items()}
        self.assertEqual({self.key: self.value}, decoded_annotations)