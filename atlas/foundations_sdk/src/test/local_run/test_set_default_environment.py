
from foundations_spec import *
from foundations.local_run import *
import fakeredis
import sys

class TestSetDefaultEnvironment(Spec):

    mock_environment_fetcher = let_patch_instance('foundations_core_cli.environment_fetcher.EnvironmentFetcher')
    mock_uuid4 = let_patch_mock('uuid.uuid4')
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')
    mock_at_exit = let_patch_mock('atexit.register')
    mock_upload_artifacts = let_patch_mock('foundations_contrib.archiving.upload_artifacts.upload_artifacts')
    mock_run_job_klass = let_patch_mock_with_conditional_return('foundations_events.producers.jobs.RunJob')
    mock_run_job = let_mock()
    mock_complete_job_klass = let_patch_mock_with_conditional_return('foundations_events.producers.jobs.CompleteJob')
    mock_complete_job = let_mock()
    mock_failed_job_klass = let_patch_mock_with_conditional_return('foundations_events.producers.jobs.FailedJob')
    mock_failed_job = let_mock()
    mock_original_exception_hook = let_patch_mock('sys.__excepthook__')

    @let_now
    def mock_logger(self):
        return Mock()

    @let_now
    def mock_config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return self.patch('foundations_contrib.global_state.config_manager', ConfigManager())

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.global_state.log_manager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.local_run')
        mock.return_when(self.mock_logger, 'foundations_contrib.config_manager')
        return mock

    @let_now
    def mock_os_environment(self):
        return self.patch('os.environ', {})

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

    @let
    def override_project_name(self):
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
    def override_job_id(self):
        return self.faker.uuid4()

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

    mock_config_listing_klass = let_patch_mock_with_conditional_return('foundations_core_cli.typed_config_listing.TypedConfigListing')

    @let
    def mock_config_listing(self):
        mock = ConditionalReturn()
        mock.config_path.return_when(None, 'default')
        mock.update_config_manager_with_config = Mock()
        return mock

    @set_up
    def set_up(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (['/path/to/default.config.yaml'], [])
        self.mock_message_router.push_message.side_effect = self._push_message
        self.mock_at_exit.side_effect = self._register_at_exit
        
        self.message = None
        self.at_exit = None

        self.mock_run_job_klass.return_when(self.mock_run_job, self.mock_message_router, self.foundations_context)
        self.mock_complete_job_klass.return_when(self.mock_complete_job, self.mock_message_router, self.foundations_context)
        self.mock_failed_job_klass.return_when(self.mock_failed_job, self.mock_message_router, self.foundations_context, self.exception_data)

        self.mock_config_listing_klass.return_when(self.mock_config_listing, 'execution')

        self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

        sys.excepthook = sys.__excepthook__

    @tear_down
    def tear_down(self):
        sys.excepthook = sys.__excepthook__

    def test_job_environment_set_up_when_default_environment_present(self):
        self.patch('foundations.local_run.load_execution_environment', return_value=True)
        mock_set_up_environment = self.patch('foundations.local_run.set_up_job_environment')
        set_up_default_environment_if_present()
        mock_set_up_environment.assert_called()

    def test_load_execution_environment_returns_true_when_execution_default_present(self):
        self._set_up_config_listing_mock()
        self.assertEqual(True, load_execution_environment())

    def test_load_execution_environment_updates_global_config_with_default_execution_config(self):
        from foundations_internal.config.execution import translate

        self._set_up_config_listing_mock()
        load_execution_environment()
        self.mock_config_listing.update_config_manager_with_config.assert_called_with('default', translate)

    def test_load_execution_environment_returns_false_when_absent(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], [])
        self.assertEqual(False, load_execution_environment())

    def test_load_execution_environment_returns_false_when_no_environments(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (None, None)
        self.assertEqual(False, load_execution_environment())

    def test_treats_running_process_like_deployment(self):
        set_up_job_environment()
        self.assertEqual(True, self.mock_config_manager['_is_deployment'])

    def test_default_config_file_contents_are_logged(self):        
        self.mock_environment_fetcher.get_all_environments.return_value = (['/path/to/default.config.yaml'], [])
        set_up_job_environment()
        self.mock_logger.debug.assert_called_with(
            'Foundations has been run with the following configuration:\n'
            '_is_deployment: true\nrun_script_environment: {}\n'
        )

    def test_warns_when_default_environment_not_present_and_not_in_command_line(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], [])
        set_up_default_environment_if_present()
        self.mock_logger.warn.assert_called_with(
            'Foundations has been imported, but no default configuration file has been found. '
            'Refer to the documentation for more information. '
            'Without a default configuration file, no foundations code will be executed.')

    def test_sets_default_job_id(self):
        set_up_job_environment()
        self.assertEqual(self.random_uuid, self.pipeline_context.file_name)

    def test_sets_override_job_id(self):
        self.mock_os_environment['FOUNDATIONS_JOB_ID'] = self.override_job_id
        set_up_job_environment()
        self.assertEqual(self.override_job_id, self.pipeline_context.file_name)

    def test_pushes_queued_job_message_with_project_name_set(self):
        set_up_job_environment()
        self.assertEqual(self.directory_base, self.message['project_name'])

    def test_pushes_queued_job_message_with_project_name_set_using_environment_variable(self):
        self.mock_os_environment['FOUNDATIONS_PROJECT_NAME'] = self.override_project_name
        set_up_job_environment()
        self.assertEqual(self.override_project_name, self.message['project_name'])

    def test_registers_artifact_upload_handler_at_exit(self):
        set_up_job_environment()
        self.at_exit()
        self.mock_upload_artifacts.assert_called_with(self.random_uuid)

    def test_registers_job_completion_handler_at_exit(self):
        set_up_job_environment()
        self.at_exit()
        self.mock_complete_job.push_message.assert_called()

    def test_registers_job_failure_handler_at_exit(self):
        set_up_job_environment()
        sys.excepthook(None, None, None)
        self.at_exit()
        self.mock_failed_job.push_message.assert_called()

    def test_does_not_register_failure_if_no_exception_raised(self):
        set_up_job_environment()
        self.at_exit()
        self.mock_failed_job.push_message.assert_not_called()

    def test_does_not_register_failure_if_process_not_finished(self):
        set_up_job_environment()
        sys.excepthook(None, None, None)
        self.mock_failed_job.push_message.assert_not_called()

    def test_calls_original_exception_hook(self):
        set_up_job_environment()

        error_type = Mock()
        error_value = Mock()
        traceback = Mock()
        sys.excepthook(error_type, error_value, traceback)
        self.mock_original_exception_hook.assert_called_with(error_type, error_value, traceback)

    def test_does_not_immediately_call_complete_job(self):
        set_up_job_environment()
        self.mock_complete_job.push_message.assert_not_called()

    def test_marks_job_as_running(self):
        set_up_job_environment()
        self.mock_run_job.push_message.assert_called()

    def test_does_not_register_completion_if_exception_raised(self):
        set_up_job_environment()
        sys.excepthook(None, None, None)
        self.at_exit()
        self.mock_complete_job.push_message.assert_not_called()

    def _set_up_config_listing_mock(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], [])
        self.mock_config_listing.config_path.clear()
        self.mock_config_listing.config_path.return_when(self.faker.uri_path(), 'default')

    def _register_at_exit(self, callback):
        self.at_exit = callback

    def _push_message(self, route_name, message):
        self.assertEqual('queue_job', route_name)
        self.message = message