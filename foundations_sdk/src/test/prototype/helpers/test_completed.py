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
    
    redis = let_mock()

    @let
    def listing(self):
        return self.faker.sha256()

    @set_up
    def set_up(self):
        self.redis.smembers = ConditionalReturn()
        self.redis.smembers.return_when(self.listing, 'projects:global:jobs:completed')

    def test_returns_all_completed_job(self):
        from foundations.prototype.helpers.completed import list_jobs
        self.assertEqual(self.listing, list_jobs(self.redis))