
from foundations_spec import *
from foundations_contrib.global_metric_logger import GlobalMetricLogger, global_metric_logger_for_job

class TestGlobalMetricLogger(Spec):

    mock_current_foundations_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')
    mock_logger = let_mock()

    class MockMessageRouter(object):
        
        def __init__(self):
            self.logged_metrics = []

        def push_message(self, name, message):
            self.logged_metrics.append({name: message})

    @let
    def fake_metric_name(self):
        return self.faker.word()

    @let
    def fake_metric_value(self):
        return self.faker.random.random()

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    @let
    def fake_project_name(self):
        return self.faker.word()

    @let
    def message(self):
        return {
            'project_name': self.fake_project_name, 
            'job_id': self.fake_job_id, 
            'key': self.fake_metric_name, 
            'value': self.fake_metric_value
        }

    @let
    def fake_metric_name_2(self):
        return self.faker.word()

    @let
    def fake_metric_value_2(self):
        return self.faker.random.random()

    @let
    def message_2(self):
        return {
            'project_name': self.fake_project_name, 
            'job_id': self.fake_job_id, 
            'key': self.fake_metric_name_2, 
            'value': self.fake_metric_value_2
        }

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations_contrib.global_metric_logger')
        return mock

    @set_up
    def set_up(self):
        from foundations_internal.pipeline_context import PipelineContext

        self._pipeline_context = PipelineContext()
        self.mock_current_foundations_context.pipeline_context.return_value = self._pipeline_context

        def mock_is_in_running_job():
            try:
                return self._pipeline_context.file_name is not None
            except ValueError:
                return False

        self.mock_current_foundations_context.is_in_running_job = mock_is_in_running_job

        self._message_router = self.MockMessageRouter()
        self._logger = GlobalMetricLogger(self._message_router)

        self._pipeline_context.file_name = None
        self._pipeline_context.provenance.project_name = self.fake_project_name
        self.mock_current_foundations_context.project_name = self._pipeline_context.provenance.project_name

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import log_manager
        log_manager.set_foundations_not_running_warning_printed(False)

    def test_log_metric_stores_metric(self):
        self._pipeline_context.file_name = self.fake_job_id
        self.mock_current_foundations_context.job_id = self._pipeline_context.file_name
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([{'job_metrics': self.message}], self._logged_metrics())

    def test_log_metric_shows_warning_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        self.mock_current_foundations_context.job_id = None
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_with('Script not run with Foundations.')

    def test_log_metric_shows_warning_only_once_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        self.mock_current_foundations_context.job_id = None
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_once_with('Script not run with Foundations.')

    def test_log_metric_does_not_show_warning_if_in_running_job(self):
        self._pipeline_context.file_name = self.fake_job_id
        self.mock_current_foundations_context.job_id = self._pipeline_context.file_name
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_not_called()

    def test_log_metric_can_log_multiple_messages(self):
        self._pipeline_context.file_name = self.fake_job_id
        self.mock_current_foundations_context.job_id = self._pipeline_context.file_name
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self._logger.log_metric(self.fake_metric_name_2, self.fake_metric_value_2)
        self.assertEqual([{'job_metrics': self.message}, {'job_metrics': self.message_2}], self._logged_metrics())

    def test_log_metric_does_not_log_anything_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        self.mock_current_foundations_context.job_id = None
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([], self._logged_metrics())

    def test_global_metric_logger_for_job_constructs_global_metric_logger_with_current_message_router(self):
        from foundations_contrib.global_state import message_router

        mock_global_metric_logger_class = self.patch('foundations_contrib.global_metric_logger.GlobalMetricLogger', ConditionalReturn())
        mock_global_metric_logger = Mock()
        mock_global_metric_logger_class.return_when(mock_global_metric_logger, message_router)
        self.assertEqual(mock_global_metric_logger, global_metric_logger_for_job())

    def _logged_metrics(self):
        return self._message_router.logged_metrics