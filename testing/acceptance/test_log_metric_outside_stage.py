"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
import foundations
from pandas.testing import assert_frame_equal

class TestLogMetricOutsideStage(Spec):

    @set_up_class
    def set_up_class(klass):
        from acceptance.cleanup import cleanup
        cleanup()

    @set_up
    def set_up(self):
        from uuid import uuid4
        from foundations_contrib.producers.jobs.queue_job import QueueJob
        from foundations_contrib.global_state import message_router, current_foundations_context

        foundations.set_project_name('default')
        self._job_id = str(uuid4())
        pipeline_context = current_foundations_context().pipeline_context()
        pipeline_context.file_name = self._job_id
        queue_job = QueueJob(message_router, pipeline_context)
        queue_job.push_message()

    def test_log_metric_outside_of_job_does_not_log_metric_but_still_executes(self):
        import subprocess

        metrics_before_script_run = self._get_metrics_for_all_jobs()
        completed_process = subprocess.run(['python', 'acceptance/fixtures/log_metric_script.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        metrics_after_script_run = self._get_metrics_for_all_jobs()

        self.assertEqual(0, completed_process.returncode)
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
        self.assertIn('Hello World!', process_output)

        logged_metric = self._get_logged_metric(self._job_id, 'key')
        self.assertEqual('value', logged_metric)

    def _get_metrics_for_all_jobs(self):
        return foundations.get_metrics_for_all_jobs('default')

    def _get_logged_metric(self, job_id, metric_name):
        all_metrics = self._get_metrics_for_all_jobs()
        metrics_for_job = all_metrics.loc[all_metrics['job_id'] == job_id].iloc[0]
        return metrics_for_job[metric_name]