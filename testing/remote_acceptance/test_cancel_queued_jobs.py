"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_spec import *

from foundations import cancel_queued_jobs

@skip('completely deprecated - to be removed')
class TestCancelQueuedJobs(Spec):

    @tear_down
    def tear_down(self):
        from remote_acceptance.cleanup import cleanup
        cleanup()
    
    @set_up
    def set_up(self):
        from foundations import config_manager
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        import remote_acceptance.config.remote_config as remote_config

        remote_config.config()

        config_manager['deployment_implementation'] = {
            'deployment_type': LocalShellJobDeployment
        }
    
    def _use_remote_deployment(self):
        from foundations import config_manager
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
        
        config_manager['deployment_implementation'] = {
            'deployment_type': SFTPJobDeployment
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

        from remote_acceptance.fixtures.stages import wait_five_seconds, finishes_instantly

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        finishes_instantly = foundations.create_stage(finishes_instantly)

        wait_five_seconds_deployment_object = wait_five_seconds().run()
        finishes_instantly_deployment_object = finishes_instantly().run()

        job_id = finishes_instantly_deployment_object.job_name()
        expected_job_cancel_status = {job_id: False}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))

    def test_cancel_succeeds_if_jobs_run_remotely(self):
        import foundations

        from remote_acceptance.fixtures.stages import wait_five_seconds, finishes_instantly
        self._use_remote_deployment()

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        finishes_instantly = foundations.create_stage(finishes_instantly)

        wait_five_seconds_deployment_object = wait_five_seconds().run()
        finishes_instantly_deployment_object = finishes_instantly().run()

        job_id = finishes_instantly_deployment_object.job_name()
        expected_job_cancel_status = {job_id: True}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))        

    def test_cancel_fails_if_job_is_completed(self):
        import foundations

        from remote_acceptance.fixtures.stages import finishes_instantly
        self._use_remote_deployment()

        finishes_instantly = foundations.create_stage(finishes_instantly)
        deployment_object = finishes_instantly().run()
        deployment_object.wait_for_deployment_to_complete()

        job_id = deployment_object.job_name()
        expected_job_cancel_status = {job_id: False}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))

    def test_cancel_job_removes_job_from_job_directory(self):
        import foundations
        from foundations import config_manager
        from foundations_ssh.sftp_bucket import SFTPBucket

        from remote_acceptance.fixtures.stages import finishes_instantly, wait_five_seconds

        self._use_remote_deployment()
        sftp_bucket = SFTPBucket(config_manager['code_path'])

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        finishes_instantly = foundations.create_stage(finishes_instantly)

        wait_five_seconds_deployment_object = wait_five_seconds().run()
        deployment_object = finishes_instantly().run()

        job_id = deployment_object.job_name()
        cancel_queued_jobs([job_id])

        job_exists = sftp_bucket.exists(job_id + '.tgz')

        self.assertFalse(job_exists)