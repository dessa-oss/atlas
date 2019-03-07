"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.spec import Spec

from foundations_contrib.consumers.jobs.completed.global_listing import GlobalListing

class TestGlobalListing(Spec):
    
    redis = let_mock()

    @let
    def consumer(self):
        return GlobalListing(self.redis)

    def test_adds_job_to_global_completed_listing(self):
        self.consumer.call({'project_name': 'my fancy project', 'job_id': 'my fantastic job'}, None, None)
        self.redis.sadd.assert_called_with('projects:global:jobs:completed', 'my fantastic job')

    def test_adds_job_to_project_completed_listing_different_job(self):
        self.consumer.call({'project_name': 'my fancy project', 'job_id': 'my sad job'}, None, None)
        self.redis.sadd.assert_called_with('projects:global:jobs:completed', 'my sad job')
