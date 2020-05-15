

from foundations_spec import *
from acceptance.mixins.metrics_fetcher import MetricsFetcher

import foundations
from pandas.testing import assert_frame_equal

class TestLogMetricOutsideStage(Spec, MetricsFetcher):

    @set_up_class
    def set_up_class(klass):
        from acceptance.cleanup import cleanup
        cleanup()

    @set_up
    def set_up(self):
        from uuid import uuid4
        from foundations_events.producers.jobs import QueueJob
        from foundations_contrib.global_state import message_router, current_foundations_job

        foundations.set_project_name('default')
        self._job_id = str(uuid4())
        current_foundations_job().job_id = self._job_id
        queue_job = QueueJob(message_router, current_foundations_job())
        queue_job.push_message()

    def test_log_metric_outside_of_job_throws_warning_and_does_not_log_metric_but_still_executes(self):
        import subprocess

        metrics_before_script_run = self._get_metrics_for_all_jobs('default')
        completed_process = subprocess.run(['python', 'acceptance/fixtures/log_metric_script.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        metrics_after_script_run = self._get_metrics_for_all_jobs('default')

        self.assertEqual(0, completed_process.returncode)
        self.assertIn('Script not run with Foundations.', process_output)
        self.assertIn('Hello World!', process_output)
        assert_frame_equal(metrics_before_script_run, metrics_after_script_run)

    def test_log_metric_in_job_logs_metric_and_runs_successfully(self):
        import os
        import subprocess

        subprocess_environment = os.environ.copy()
        subprocess_environment['ACCEPTANCE_TEST_JOB_ID'] = self._job_id

        completed_process = subprocess.run(['python', 'acceptance/fixtures/in_job_log_metric_script.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=subprocess_environment)
        process_output = completed_process.stdout.decode()

        self.assertEqual(0, completed_process.returncode)
        self.assertNotIn('Script not run with Foundations.', process_output)
        self.assertIn('Hello World!', process_output)

        logged_metric = self._get_logged_metric('default', self._job_id, 'key')
        self.assertEqual('value', logged_metric)
