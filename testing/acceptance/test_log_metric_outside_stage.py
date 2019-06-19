"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations import log_metric

@skip
class TestLogMetricOutsideStage(Spec):

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

    def test_can_run_job(self):
        from scheduler_acceptance.fixtures.stages import add_two_numbers
        import foundations

        log_metric('my_metric', 'mountains in the distance')
        add_two_numbers = foundations.create_stage(add_two_numbers)
        stage = add_two_numbers(3, 17)

        job = stage.run()
        job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        self.assertEqual('mountains in the distance', job_metrics['my_metric'].iloc[0])