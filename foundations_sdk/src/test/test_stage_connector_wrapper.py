"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.stage_connector_wrapper import StageConnectorWrapper


class TestStageConnectorWrapper(unittest.TestCase):

    class MockArgument(object):
        def __init__(self):
            self.cache_enabled = False

        def enable_caching(self):
            self.cache_enabled = True

    class MockConnector(object):

        def __init__(self, uuid):
            self._uuid = uuid
            self._args = ()
            self._kwargs = {}

        def args(self):
            return self._args

        def set_args(self, value):
            self._args = value

        def kwargs(self):
            return self._kwargs

        def set_kwargs(self, value):
            self._kwargs = value

        def uuid(self):
            return self._uuid

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.stage_context import StageContext
        from foundations.stage_config import StageConfig

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._connector = self.MockConnector(self._uuid)
        self._pipeline_context = PipelineContext()
        self._stage_context = StageContext()
        self._stage_config = StageConfig()
        self._stage = StageConnectorWrapper(
            None, self._connector, self._pipeline_context, self._stage_context, self._stage_config)

    def test_enable_caching_returns_self(self):
        self._stage.enable_caching()
        self.assertEqual(self._stage, self._stage.enable_caching())

    def test_enable_caching_forwards_call(self):
        self._stage.enable_caching()
        self.assertTrue(self._stage_config.allow_caching())

    def test_enable_caching_forwards_call_to_args(self):
        argument = self.MockArgument()
        self._connector.set_args((argument,))

        self._stage.enable_caching()
        self.assertTrue(argument.cache_enabled)

    def test_enable_caching_forwards_call_to_args_multiple_args(self):
        argument = self.MockArgument()
        argument_two = self.MockArgument()
        self._connector.set_args((argument, argument_two))

        self._stage.enable_caching()
        self.assertTrue(argument.cache_enabled)
        self.assertTrue(argument_two.cache_enabled)

    def test_enable_caching_forwards_call_to_kwargs(self):
        argument = self.MockArgument()
        self._connector.set_kwargs({'hello': argument})

        self._stage.enable_caching()
        self.assertTrue(argument.cache_enabled)

    def test_enable_caching_forwards_call_to_kwargs_multiple_kwargs(self):
        argument = self.MockArgument()
        argument_two = self.MockArgument()
        self._connector.set_kwargs({'hello': argument, 'world': argument_two})

        self._stage.enable_caching()
        self.assertTrue(argument.cache_enabled)
        self.assertTrue(argument_two.cache_enabled)
