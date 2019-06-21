"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestAnnotate(Spec):

    mock_log_manager = let_patch_mock('foundations_contrib.global_state.log_manager')

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

    def test_call_with_two_key_value_pairs_gets_saved_to_redis(self):
        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, None)
        self.consumer.call({'job_id': self.job_id, 'key': self.key_two, 'value': self.value_two}, None, None)
        result_annotations = self.redis.hgetall('jobs:{}:annotations'.format(self.job_id))
        decoded_annotations = {key.decode(): value.decode() for key, value in result_annotations.items()}
        self.assertEqual({self.key: self.value, self.key_two: self.value_two}, decoded_annotations)

    def test_call_with_same_key_and_different_values_gets_saved_to_redis(self):
        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, None)
        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value_two}, None, None)
        result_annotations = self.redis.hgetall('jobs:{}:annotations'.format(self.job_id))
        decoded_annotations = {key.decode(): value.decode() for key, value in result_annotations.items()}
        self.assertEqual({self.key: self.value_two}, decoded_annotations)

    def test_call_with_same_key_and_different_values_logs_warning(self):
        mock_logger = Mock()
        mock_get_logger = ConditionalReturn()
        mock_get_logger.return_when(mock_logger, 'foundations_contrib.consumers.annotate')
        self.mock_log_manager.get_logger = mock_get_logger

        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value}, None, None)
        self.consumer.call({'job_id': self.job_id, 'key': self.key, 'value': self.value_two}, None, None)
        result_annotations = self.redis.hgetall('jobs:{}:annotations'.format(self.job_id))
        decoded_annotations = {key.decode(): value.decode() for key, value in result_annotations.items()}

        mock_logger.warning.assert_called_with('Tag `{}` updated to `{}`'.format(self.key, self.value_two))