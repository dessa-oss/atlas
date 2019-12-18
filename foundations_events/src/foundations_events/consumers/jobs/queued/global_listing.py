"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_events.consumers.jobs.mixins.listing import Listing


class GlobalListing(Listing):
    """Saves the job to a list of queued jobs for a project in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _scope(self):
        return 'projects'

    def _listing_name(self):
        return 'jobs:queued'

    def _scope_value(self, message):
        return 'global'

    def _listing_value(self, message):
        return message['job_id']