"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import MagicMock, patch
from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
import redis


class TestRedisPipelineWrapper(unittest.TestCase):

    def setUp(self):
        self._pipe = MagicMock()

    class MockPipe(object):
        def get(self, *args, **kwargs):
            return

        def smembers(self, *args, **kwargs):
            return

        def execute(self, *args, **kwargs):
            return [1, 2]

    def test_get_attr_gets_attribute(self):
        mock_pipe = self.MockPipe()
        pipe = RedisPipelineWrapper(mock_pipe)
        pipe.get('hello')

    def test_get_attr_gets_attribute_different_attribute(self):
        mock_pipe = self.MockPipe()
        pipe = RedisPipelineWrapper(mock_pipe)
        pipe.smembers('hello')

    def test_get_attr_raises_attribute_error(self):
        mock_pipe = self.MockPipe()
        pipe = RedisPipelineWrapper(mock_pipe)
        with self.assertRaises(AttributeError) as context:
            pipe.wave('hello')
        self.assertIn("'MockPipe' object has no attribute 'wave'",
                      context.exception.args)

    def test_get_attr_returns_a_promise(self):
        import promise
        pipe = RedisPipelineWrapper(self._pipe)
        result = pipe.get('potato')
        self.assertTrue(isinstance(result, promise.Promise))

    def test_get_attr_returns_a_promise_different_command(self):
        import promise
        pipe = RedisPipelineWrapper(self._pipe)
        result = pipe.smembers('rainbow')
        self.assertTrue(isinstance(result, promise.Promise))

    def test_executes_pipeline(self):
        pipe = RedisPipelineWrapper(self._pipe)
        pipe.execute()
        self._pipe.execute.assert_called_once()

    def test_execute_pipeline_assigns_correct_return(self):
        mock_pipe = self.MockPipe()
        pipe = RedisPipelineWrapper(mock_pipe)
        command_1 = pipe.smembers('rainbow')
        command_2 = pipe.smembers('sunshine')
        pipe.execute()
        self.assertEqual(command_1.get(), 1)
        self.assertEqual(command_2.get(), 2)
