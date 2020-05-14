
from foundations_spec import *
from acceptance.mixins.metrics_fetcher import MetricsFetcher

import foundations

class TestAnnotateWithoutStage(Spec, MetricsFetcher):

    @let
    def annotations(self):
        return {
            'model type': 'simple mlp',
            'data set': 'out of time',
            'what I was doing,': 'drinking tea'
        }

    @set_up
    def set_up(self):
        from uuid import uuid4
        from foundations_events.producers.jobs import QueueJob
        from foundations_contrib.global_state import message_router, current_foundations_context
        from acceptance.cleanup import cleanup

        cleanup()

        foundations.set_project_name('default')
        self._job_id = str(uuid4())
        current_foundations_context().job_id = self._job_id
        queue_job = QueueJob(message_router, current_foundations_context())
        queue_job.push_message()

    def test_set_tag_outside_of_job_throws_warning_and_does_not_set_tag_but_still_executes(self):
        import subprocess
        from pandas.testing import assert_frame_equal

        metrics_before_script_run = self._get_metrics_and_tags_for_all_jobs('default', ignore_errors=True)
        completed_process = subprocess.run(['python', 'acceptance/fixtures/set_annotation_script.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        metrics_after_script_run = self._get_metrics_and_tags_for_all_jobs('default', ignore_errors=True)

        self.assertEqual(0, completed_process.returncode)
        self.assertIn('Script not run with Foundations.', process_output)
        self.assertIn('Hello World!', process_output)
        assert_frame_equal(metrics_before_script_run, metrics_after_script_run)

    def test_set_tag_in_job_sets_tag_and_runs_successfully(self):
        completed_process = self._run_job_with_annotations()
        process_output = completed_process.stdout.decode()

        self.assertEqual(0, completed_process.returncode)
        self.assertNotIn('Script not run with Foundations.', process_output)
        self.assertIn('Hello World!', process_output)
        self._assert_tags_set()

    def test_can_retrieve_metrics_in_old_format(self):
        from pandas.testing import assert_frame_equal

        self._run_job_with_annotations()

        metrics = self._get_metrics_for_all_jobs('default')
        job_metrics = self._metrics_for_job(metrics)

        prototype_metrics = self._get_metrics_and_tags_for_all_jobs('default')
        prototype_metrics = prototype_metrics[list(job_metrics)]
        prototype_job_metrics = self._metrics_for_job(prototype_metrics)

        assert_frame_equal(job_metrics, prototype_job_metrics)

    def _metrics_for_job(self, metrics):
        return metrics[metrics['job_id'] == self._job_id].iloc[[0]]

    def _run_job_with_annotations(self):
        import os
        import subprocess

        subprocess_environment = os.environ.copy()
        subprocess_environment['ACCEPTANCE_TEST_JOB_ID'] = self._job_id

        return subprocess.run(['python', 'acceptance/fixtures/in_job_set_annotation_script.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=subprocess_environment)

    def _assert_tags_set(self):
        for tag_name, expected_tag_value in self.annotations.items():
            actual_tag_value = self._get_tag('default', self._job_id, tag_name)
            self.assertEqual(expected_tag_value, actual_tag_value)

