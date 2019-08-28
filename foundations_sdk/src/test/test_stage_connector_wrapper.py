"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations.stage_connector_wrapper import StageConnectorWrapper
from foundations_internal.deployment_manager import DeploymentManager
from mock import patch, call

class TestStageConnectorWrapper(Spec):

    mock_foundations_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')

    @let
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        config_manager = ConfigManager()
        return self.patch('foundations.config_manager', config_manager)

    class MockArgument(object):
        def __init__(self):
            self.cache_enabled = False

        def enable_caching(self):
            self.cache_enabled = True

    class MockStage(object):

        def __init__(self, uuid):
            self._uuid = uuid
            self._args = ()
            self._kwargs = {}

        def stage_args(self):
            return self._args

        def set_args(self, value):
            self._args = value

        def stage_kwargs(self):
            return self._kwargs

        def set_kwargs(self, value):
            self._kwargs = value

        def uuid(self):
            return self._uuid

    def setUp(self):
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_internal.stage_context import StageContext
        from foundations_internal.stage_config import StageConfig

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._connector = self.MockStage(self._uuid)
        self._pipeline_context = PipelineContext()
        self._stage_context = StageContext()
        self._stage_config = StageConfig()
        self._stage = StageConnectorWrapper(
            self._connector, self._pipeline_context, self._stage_context, self._stage_config)

        self.mock_foundations_context.is_in_running_job.return_value = False

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

    class MockDeploymentWrapper(object):
        def __init__(self, deployment):
            self._deployment = deployment
            self._job_name = 'potato'

        def job_name(self):
            return self._job_name

    @patch('foundations_contrib.deployment_wrapper.DeploymentWrapper', MockDeploymentWrapper)
    @patch.object(DeploymentManager, 'simple_deploy')
    def test_run_in_a_running_stageless_job_throws_exception(self, _):
        self.mock_foundations_context.is_in_running_job.return_value = True

        with self.assertRaises(RuntimeError) as error_context:
            self._stage.run()

        self.assertIn('Cannot create stages in a running stageless job - was code written with stages deployed in a stageless job?', error_context.exception.args)

    @patch('foundations_contrib.deployment_wrapper.DeploymentWrapper', MockDeploymentWrapper)
    @patch.object(DeploymentManager, 'simple_deploy')
    def test_run_does_not_throw_exception_when_enable_stages_is_true_and_job_id_is_set(self, _):
        self.mock_foundations_context.is_in_running_job.return_value = True
        self.config_manager['run_script_environment'] = {'enable_stages': True}

        with self.assert_does_not_raise():
            self._stage.run()

    @patch('foundations_contrib.deployment_wrapper.DeploymentWrapper', MockDeploymentWrapper)
    @patch.object(DeploymentManager, 'simple_deploy')
    @patch('logging.Logger.info')
    def test_run_logging(self, logger_mock, deployment_mock):
        deployment_mock.return_value = 'something'
        self._stage.run()
        logger_mock.assert_called_with("Deploying job...")
