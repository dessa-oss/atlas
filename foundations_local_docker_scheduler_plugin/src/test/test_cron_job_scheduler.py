"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestCronJobScheduler(Spec):

    mock_put = let_patch_mock('requests.put')

    @let
    def scheduler_host(self):
        return self.faker.hostname()

    @let
    def scheduler_port(self):
        return self.faker.random.randint(80, 30000)

    @let
    def scheduler_uri(self):
        return f'http://{self.scheduler_host}:{self.scheduler_port}'

    @let
    def default_scheduler_uri(self):
        return f'http://localhost:5000'

    @let
    def scheduler(self):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler
        return CronJobScheduler(host=self.scheduler_host, port=self.scheduler_port)

    @let
    def scheduler_default_args(self):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler
        return CronJobScheduler()

    @let
    def job_id(self):
        return self.faker.word()

    def test_pause_scheduled_job_calls_correct_endpoint(self):
        self.scheduler.pause_job(self.job_id)

        request_payload = {'status': 'paused'}
        self.mock_put.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', json=request_payload)