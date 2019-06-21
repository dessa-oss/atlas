"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers import *
from foundations_spec.helpers.spec import Spec
import foundations
import foundations.prototype

class TestAnnotateWithoutStage(Spec):

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
        from foundations_contrib.producers.jobs.queue_job import QueueJob
        from foundations_contrib.global_state import message_router, current_foundations_context
        from acceptance.cleanup import cleanup

        cleanup()

        foundations.set_project_name('default')
        self._job_id = str(uuid4())
        pipeline_context = current_foundations_context().pipeline_context()
        pipeline_context.file_name = self._job_id
        queue_job = QueueJob(message_router, pipeline_context)
        queue_job.push_message()

    def test_set_tag_outside_of_job_throws_warning_and_does_not_set_tag_but_still_executes(self):
        import subprocess
        from pandas.testing import assert_frame_equal

        metrics_before_script_run = self._get_metrics_for_all_jobs()
        completed_process = subprocess.run(['python', 'acceptance/fixtures/set_annotation_script.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        metrics_after_script_run = self._get_metrics_for_all_jobs()

        self.assertEqual(0, completed_process.returncode)
        self.assertIn('Cannot set tag if not deployed with foundations deploy', process_output)
        self.assertIn('Hello World!', process_output)
        assert_frame_equal(metrics_before_script_run, metrics_after_script_run)

    def test_set_tag_in_job_sets_tag_and_runs_successfully(self):
        completed_process = self._run_job_with_annotations()
        process_output = completed_process.stdout.decode()

        self.assertEqual(0, completed_process.returncode)
        self.assertNotIn('Cannot set tag if not deployed with foundations deploy', process_output)
        self.assertIn('Hello World!', process_output)
        self._assert_tags_set()

    def test_can_retrieve_metrics_in_old_format(self):
        from pandas.testing import assert_frame_equal

        self._run_job_with_annotations()

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == self._job_id].loc[[0]]

        prototype_metrics = self._get_metrics_for_all_jobs()
        prototype_metrics = prototype_metrics[list(job_metrics)]
        prototype_job_metrics = prototype_metrics[prototype_metrics['job_id'] == self._job_id].loc[[0]]

        assert_frame_equal(job_metrics, prototype_job_metrics)

    def _run_job_with_annotations(self):
        import os
        import subprocess

        subprocess_environment = os.environ.copy()
        subprocess_environment['ACCEPTANCE_TEST_JOB_ID'] = self._job_id

        return subprocess.run(['python', 'acceptance/fixtures/in_job_set_annotation_script.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=subprocess_environment)

    def _assert_tags_set(self):
        metrics_for_job = self._get_metrics_for_job()

        for tag_name, expected_tag_value in self.annotations.items():
            actual_tag_value = self._get_tag(metrics_for_job, tag_name)
            self.assertEqual(expected_tag_value, actual_tag_value)

    def _get_metrics_for_all_jobs(self):
        import pandas

        try:
            return foundations.prototype.get_metrics_for_all_jobs('default')
        except KeyError as ex:
            if 'job_id' in ex.args:
                return pandas.DataFrame()
            raise

    def _get_metrics_for_job(self):
        all_metrics = self._get_metrics_for_all_jobs()
        return all_metrics.loc[all_metrics['job_id'] == self._job_id].iloc[0]

    def _get_tag(self, metrics_for_job, tag):
        return metrics_for_job['tag_{}'.format(tag)]