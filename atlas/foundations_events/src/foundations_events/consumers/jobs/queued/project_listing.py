
from foundations_events.consumers.jobs.mixins.listing import Listing


class ProjectListing(Listing):
    """Saves the job to a list of running jobs for a project in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _scope(self):
        return 'project'

    def _listing_name(self):
        return 'jobs:running'

    def _scope_value(self, message):
        return message['project_name']

    def _listing_value(self, message):
        return message['job_id']
