"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn

class TestCompletedJobHelpers(Spec):
    
    @let
    def redis(self):
        from fakeredis import FakeRedis
        return FakeRedis()

    @let
    def listing(self):
        return {self._random_uuid() for _ in range(self.job_count)}

    @let
    def job_count(self):
        import random
        return random.randint(1, 10)

    @set_up
    def set_up(self):
        for job_id in self.listing:
            self.redis.sadd('projects:global:jobs:completed', job_id)

    def test_returns_all_completed_job(self):
        from foundations.prototype.helpers.completed import list_jobs
        self.assertEqual(self.listing, list_jobs(self.redis))

    def _random_uuid(self):
        from uuid import uuid4
        return str(uuid4())