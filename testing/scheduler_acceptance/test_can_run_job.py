"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

class TestCanRunJob(Spec):

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

    def test_can_run_job(self):
        from scheduler_acceptance.fixtures.stages import add_two_numbers
        from foundations_contrib.global_state import redis_connection
        import foundations

        job = foundations.submit(job_directory='scheduler_acceptance/fixtures/boring_job', num_gpus=0)
        job_id = job.job_name()
        job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('boring_job')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        self.assertEqual(20, job_metrics['my_metric'].iloc[0])

    @staticmethod
    def _log_a_metric(value):
        log_metric('my_metric', value)