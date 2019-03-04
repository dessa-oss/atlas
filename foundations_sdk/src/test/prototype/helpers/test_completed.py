"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.extensions import *
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn

import random

class TestCompletedJobHelpers(Spec):
    
    redis = let_fake_redis()

    @let
    def listing(self):
        return {self._random_uuid() for _ in range(self.job_count)}

    @let
    def job_count(self):
        import random
        return random.randint(1, 10)

    @let
    def random_job_id(self):
        return random.choice(list(self.listing))

    @let
    def random_job_id_two(self):
        return random.choice(list(self.listing))

    @set_up
    def set_up(self):
        for job_id in self.listing:
            self.redis.sadd('projects:global:jobs:completed', job_id)

    def test_list_jobs_returns_all_completed_jobs(self):
        from foundations.prototype.helpers.completed import list_jobs
        self.assertEqual(self.listing, list_jobs(self.redis))

    def test_remove_jobs_removes_all_completed_jobs(self):
        from foundations.prototype.helpers.completed import remove_jobs, list_jobs
        remove_jobs(self.redis, [self.random_job_id])
        self.assertEqual(self.listing - {self.random_job_id}, list_jobs(self.redis))

    def test_remove_jobs_removes_all_completed_jobs_multiple_jobs(self):
        from foundations.prototype.helpers.completed import remove_jobs, list_jobs
        remove_jobs(self.redis, [self.random_job_id, self.random_job_id_two])
        self.assertEqual(self.listing - {self.random_job_id, self.random_job_id_two}, list_jobs(self.redis))

    def _random_uuid(self):
        from uuid import uuid4
        return str(uuid4())