"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

from foundations_spec import *
from foundations import create_stage

@skip
class TestSchedulerJobs(Spec):
    
    @let
    def job_source_bundle(self):
        from foundations_contrib.job_source_bundle import JobSourceBundle
        return JobSourceBundle(self.job_id, '../')

    @let
    def job_id(self):
        from uuid import uuid4
        return str(uuid4())

    @let
    def job(self):
        from foundations.job import Job
        return Job(self.stage)

    @let
    def stage(self):
        @create_stage
        def _callback():
            pass
        return _callback

    @let
    def deployment(self):
        from foundations_scheduler_plugin.job_deployment import JobDeployment
        return JobDeployment(self.job_id, self.job, self.job_source_bundle)

    @let
    def deployment_wrapper(self):
        from foundations.deployment_wrapper import DeploymentWrapper
        return DeploymentWrapper(self.deployment)

    @set_up
    def set_up(self):
        self.deployment.deploy()
        self._wait_for_job_to_complete()

    def test_runs_job(self):
        self.assertEqual('complete', self.deployment_wrapper.get_job_status())

    def test_creates_log(self):
        self.assertIn('Completed', self.deployment_wrapper.get_job_logs())

    def _wait_for_job_to_complete(self):
        from time import sleep

        for _ in range(60):
            if self.deployment_wrapper.is_job_complete():
                break
            sleep(1)
        
        raise AssertionError('Job did not complete')