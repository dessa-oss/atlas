"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class Scheduler(object):
    """This class models a scheduler, which (currently) only keeps track of jobs that are queued, running, and completed.  Requires a backend to function.
        Arguments:
            scheduler_backend: {*Backend} -- The backend to use with the scheduler.
    """

    def __init__(self, scheduler_backend=None):
        if not scheduler_backend:
            from foundations.scheduler_legacy_backend import LegacyBackend
            self._backend = LegacyBackend.create_default() # requires foundations_ssh
        else:
            self._backend = scheduler_backend

    def get_job_information(self, status=None):
        """Get a generator for all jobs with a certain status (or all jobs).
            Arguments:
                status: {str} -- The status to filter on.  If None, get all jobs.  Defaults to None.

        Returns:
            generator -- An iterable that yields foundations.scheduler_job_information.JobInformation objects.  Handles pagination internally.
        """

        for job_information in self._backend.get_paginated(None, None, status):
            yield job_information