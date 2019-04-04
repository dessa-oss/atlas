"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

from foundations_spec import *
from foundations import create_stage

class TestSchedulerJobs(Spec):
    
    @let
    def job_source_bundle(self):
        from foundations_contrib.job_source_bundle import JobSourceBundle
        return JobSourceBundle.for_deployment()

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

        return _callback()

    @let
    def deployment(self):
        from foundations_scheduler_plugin.job_deployment import JobDeployment
        return JobDeployment(self.job_id, self.job, self.job_source_bundle)

    @let
    def deployment_wrapper(self):
        from foundations.deployment_wrapper import DeploymentWrapper
        return DeploymentWrapper(self.deployment)

    @let
    def redis_ip(self):
        docker_adapter = self._get_docker_adapter()
        
        for ip in docker_adapter.ips:
            if isinstance(ip.ip, str):
                return ip.ip

    def _get_docker_adapter(self):
        import ifaddr

        for adapter in ifaddr.get_adapters():
            if adapter.name == 'docker0':
                return adapter

    @set_up
    def set_up(self):
        self.load_config()
        self.deployment.deploy()
        self._wait_for_job_to_complete()

    def test_runs_job(self):
        self.assertEqual('completed', self.deployment_wrapper.get_job_status())

    def test_creates_log(self):
        self.assertIn('Finished stage', self.deployment_wrapper.get_job_logs())
    
    def load_config(self):
        import os
        from foundations_contrib.global_state import config_manager
        config_manager['remote_host'] = 'localhost'
        config_manager['remote_user'] = 'job-uploader'
        config_manager['port'] = 31222
        config_manager['key_path'] = os.path.expanduser('~/.ssh/id_foundations_scheduler')
        config_manager['code_path'] = '/jobs'
        config_manager['redis_url'] = 'redis://{}:6379'.format(self.redis_ip)

    def _wait_for_job_to_complete(self):
        from time import sleep

        for _ in range(60):
            if self.deployment_wrapper.is_job_complete():
                return
            sleep(1)
        
        job_logs = self.deployment_wrapper.get_job_logs()
        raise AssertionError('Job did not complete:\n{}'.format(job_logs))