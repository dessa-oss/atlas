"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_spec.extensions import let_fake_redis
from foundations_contrib.jobs.kubernetes_job import cancel
from foundations_contrib.consumers.jobs.running.project_listing import ProjectListing
from foundations_contrib.consumers.jobs.queued.project_name import ProjectName
import foundations_contrib

class TestKubernetesJob(Spec):

    mock_subprocess_run = let_patch_mock('subprocess.run')
    redis = let_fake_redis()

    @let
    def project_name(self):
        return self.faker.sentence()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        self.patch('foundations_contrib.global_state.redis_connection', self.redis)
        ProjectListing(self.redis).call({'project_name': self.project_name, 'job_id': self.job_id}, 0, {})
        ProjectName(self.redis).call({'project_name': self.project_name, 'job_id': self.job_id}, 0, {})

    def test_cancel_deletes_job(self):
        cancel(self.job_id)
        self.mock_subprocess_run.assert_called_with(['bash', './delete_job.sh', self.job_id], cwd=foundations_contrib.root() / 'resources/jobs')

    def test_cancel_removes_job_from_global_listing(self):
        cancel(self.job_id)
        self.assertFalse(self.redis.sismember(f'project:{self.project_name}:jobs:running', self.job_id))
