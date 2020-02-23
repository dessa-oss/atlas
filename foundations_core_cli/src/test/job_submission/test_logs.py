
from foundations_spec import *

from foundations_core_cli.job_submission.logs import stream_job_logs

class TestJobSubmissionLogs(Spec):
    
    deployment = let_mock()
    mock_get_logger = let_patch_mock_with_conditional_return('foundations_contrib.global_state.log_manager.get_logger')
    mock_logger = let_mock()
    print_mock = let_patch_mock('builtins.print')
    mock_sleep = let_patch_mock('time.sleep')
    
    @let
    def mock_environment(self):
        return self.patch('os.environ', self.faker.pydict())

    @let
    def log_stream(self):
        return self.faker.sentences()

    @let
    def log_stream_with_run_time_error(self):
        log_stream = self.log_stream
        log_stream.append('RuntimeError X')
        return log_stream

    @set_up
    def set_up(self):
        self.deployment.stream_job_logs.return_value = self.log_stream
        self.mock_get_logger.return_when(self.mock_logger, 'foundations_core_cli.job_submission.logs')

    def test_logs_user_feedback_when_streaming_started(self):
        stream_job_logs(self.deployment)
        self.mock_logger.info.assert_has_calls([call('Job queued. Ctrl-C to stop streaming - job will not be interrupted or cancelled.'), call('Job running, streaming logs.')])

    def test_prints_log_stream(self):
        stream_job_logs(self.deployment)
        calls = [call(item) for item in self.log_stream]
        self.print_mock.assert_has_calls(calls)

    def test_does_not_log_job_running_if_no_stream_items(self):
        self.log_stream.clear()
        stream_job_logs(self.deployment)
        self.assertNotIn(call('Job is running; streaming logs'), self.mock_logger.info.mock_calls)

    def test_does_not_log_job_running_multiple_times(self):
        stream_job_logs(self.deployment)
        self.assertEqual(2, len(self.mock_logger.info.mock_calls))

    def test_does_not_log_if_streaming_disabled(self):
        self.mock_environment['DISABLE_LOG_STREAMING'] = 'True'
        stream_job_logs(self.deployment)
        self.mock_logger.info.assert_not_called()

    def test_sleeps_for_1_sec_before_streaming(self):
        stream_job_logs(self.deployment)
        self.mock_sleep.assert_called_with(1)

    def test_log_runtime_error_in_error_produces_system_exit_with_correct_error_message(self):
        self.deployment.stream_job_logs.return_value = self.log_stream_with_run_time_error
        
        mock_sys_exit = self.patch('sys.exit')
        stream_job_logs(self.deployment)
        calls = [call(item) for item in self.log_stream_with_run_time_error]

        mock_sys_exit.assert_called_with('RuntimeError X')