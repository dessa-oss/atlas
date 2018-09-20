"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations.scheduler_legacy_backend import LegacyBackend


class NullSchedulerBackend(LegacyBackend):

    def __init__(self):
        """Default implementation for scheduler job information for use when no backend is supported
        """

        pass

    def get_paginated(self, start_index, number_to_get, status):
        """Default implementation for scheduler job information for use when no backend is supported

        Arguments:
            start_index {int} -- Unused
            number_to_get {int} -- Unused
            status {str} -- Unused

        Returns:
            generator -- An iterable containing the jobs as specified by the arguments.
        """

        return []
