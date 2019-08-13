"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.local_run import load_local_configuration_if_present
import sys

class SetDefaultEnvironment(Spec):

    mock_environment_fetcher = let_patch_instance('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher')
    mock_set_environment = let_patch_mock('foundations.config.set_environment')
    mock_uuid4 = let_patch_mock('uuid.uuid4')
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')
    mock_at_exit = let_patch_mock('atexit.register')
    mock_upload_artifacts = let_patch_mock('foundations_contrib.archiving.upload_artifacts.upload_artifacts')
    mock_run_job_klass = let_patch_mock_with_conditional_return('foundations_contrib.producers.jobs.run_job.RunJob')
    mock_run_job = let_mock()
    mock_complete_job_klass = let_patch_mock_with_conditional_return('foundations_contrib.producers.jobs.complete_job.CompleteJob')
    mock_complete_job = let_mock()
    mock_failed_job_klass = let_patch_mock_with_conditional_return('foundations_contrib.producers.jobs.failed_job.FailedJob')
    mock_failed_job = let_mock()

    @let
    def exception_data(self):
        return {
            "type": Exception,
            "exception": '',
            "traceback": []
        }

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
        self.mock_environment_fetcher.get_all_environments.return_value = (['/path/to/default.config.yaml'], [])
        self.mock_message_router.push_message.side_effect = self._push_message
        self.mock_at_exit.side_effect = self._register_at_exit
        
        self.message = None
        self.at_exit = None

        self.mock_run_job_klass.return_when(self.mock_run_job, self.mock_message_router, self.pipeline_context)
        self.mock_complete_job_klass.return_when(self.mock_complete_job, self.mock_message_router, self.pipeline_context)
        self.mock_failed_job_klass.return_when(self.mock_failed_job, self.mock_message_router, self.pipeline_context, self.exception_data)

    def test_default_environment_loaded_when_present_locally(self):
        load_local_configuration_if_present()
        self.mock_set_environment.assert_called_with('default')

    def test_default_environment_loaded_when_present_globally(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], ['/different/path/to/config/default.config.yaml'])
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

    def test_registers_artifact_upload_handler_at_exit(self):
        load_local_configuration_if_present()
        self.at_exit()
        self.mock_upload_artifacts.assert_called_with(self.random_uuid)

    def test_registers_job_completion_handler_at_exit(self):
        load_local_configuration_if_present()
        self.at_exit()
        self.mock_complete_job.push_message.assert_called()

    def test_registers_job_failure_handler_at_exit(self):
        load_local_configuration_if_present()
        sys.excepthook(None, None, None)
        self.at_exit()
        self.mock_failed_job.push_message.assert_called()

    def test_does_not_register_failure_if_no_exception_raised(self):
        load_local_configuration_if_present()
        self.at_exit()
        self.mock_failed_job.push_message.assert_not_called()

    def test_does_not_register_failure_if_process_not_finished(self):
        load_local_configuration_if_present()
        sys.excepthook(None, None, None)
        self.mock_failed_job.push_message.assert_not_called()

    def test_does_not_immediately_call_complete_job(self):
        load_local_configuration_if_present()
        self.mock_complete_job.push_message.assert_not_called()

    def test_marks_job_as_running(self):
        load_local_configuration_if_present()
        self.mock_run_job.push_message.assert_called()

    def test_does_not_register_completion_if_exception_raised(self):
        load_local_configuration_if_present()
        sys.excepthook(None, None, None)
        self.at_exit()
        self.mock_complete_job.push_message.assert_not_called()

    def _register_at_exit(self, callback):
        self.at_exit = callback

    def _push_message(self, route_name, message):
        self.assertEqual('queue_job', route_name)
        self.message = message