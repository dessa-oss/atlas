"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.testing.helpers import set_up, tear_down
from foundations_internal.testing.helpers.spec import Spec

from foundations.prototype import cancel_queued_jobs

class TestCancelQueuedJobs(Spec):

    @tear_down
    def tear_down(self):
        from remote_acceptance.cleanup import cleanup
        cleanup()
    
    @set_up
    def set_up(self):
        from foundations import config_manager
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        import remote_acceptance.prototype.remote_config as remote_config

        remote_config.config()

        config_manager['deployment_implementation'] = {
            'deployment_type': LocalShellJobDeployment
        }

    def test_cancel_no_jobs_if_job_list_is_empty(self):
        cancelled_jobs_with_status = cancel_queued_jobs([])
        self.assertEqual({}, cancelled_jobs_with_status)
    
    def test_cancel_fails_if_no_jobs_queued(self):
        from uuid import uuid4

        job_list = [str(uuid4()), str(uuid4()), str(uuid4())]
        expected_job_cancel_status = {job_id: False for job_id in job_list}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs(job_list))

    def test_cancel_fails_if_jobs_run_locally(self):
        import foundations

        from remote_acceptance.prototype.fixtures.stages import wait_five_seconds, finishes_instantly

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        finishes_instantly = foundations.create_stage(finishes_instantly)

        wait_five_seconds_deployment_object = wait_five_seconds().run()
        finishes_instantly_deployment_object = finishes_instantly().run()

        job_id = finishes_instantly_deployment_object.job_name()
        expected_job_cancel_status = {job_id: False}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))