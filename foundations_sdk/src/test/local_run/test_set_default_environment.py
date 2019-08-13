"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.local_run import load_local_configuration_if_present

class SetDefaultEnvironment(Spec):

    mock_environment_fetcher = let_patch_instance('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher')
    mock_set_environment = let_patch_mock('foundations.config.set_environment')
    mock_uuid4 = let_patch_mock('uuid.uuid4')
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')

    @let
    def current_directory(self):
        return self.faker.uri_path() + '/' + self.directory_base

    @let
    def directory_base(self):
        return self.faker.name()

    @let_now
    def mock_working_directory(self):
        return self.patch('os.getcwd', return_value=self.current_directory)

    @let_now
    def random_uuid(self):
        import uuid

        value = self.faker.uuid4()
        self.mock_uuid4.return_value = uuid.UUID(value)
        return value

    @let
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()
    
    @let_now
    def foundations_context(self):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.foundations_context import FoundationsContext

        pipeline = Pipeline(self.pipeline_context)
        context = FoundationsContext(pipeline)
        return self.patch('foundations_contrib.global_state.foundations_context', context)

    @set_up
    def set_up(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (['default'], [])
        self.mock_message_router.push_message.side_effect = self._push_message
        self.message = None

    def test_default_environment_loaded_when_present_locally(self):
        load_local_configuration_if_present()
        self.mock_set_environment.assert_called_with('default')

    def test_default_environment_loaded_when_present_globally(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], ['default'])
        load_local_configuration_if_present()
        self.mock_set_environment.assert_called_with('default')

    def test_default_environment_not_loaded_when_absent(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], [])
        load_local_configuration_if_present()
        self.mock_set_environment.assert_not_called()
    
    def test_default_environment_not_loaded_when_no_environments(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (None, None)
        load_local_configuration_if_present()
        self.mock_set_environment.assert_not_called()

    def test_sets_default_job_id(self):
        load_local_configuration_if_present()
        self.assertEqual(self.random_uuid, self.pipeline_context.file_name)

    def test_pushes_queued_job_message_with_project_name_set(self):
        load_local_configuration_if_present()
        self.assertEqual(self.directory_base, self.message['project_name'])

    def _push_message(self, route_name, message):
        self.assertEqual('queue_job', route_name)
        self.message = message