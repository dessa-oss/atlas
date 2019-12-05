"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.scheduler_legacy_backend import LegacyBackend


class MockSchedulerBackend(LegacyBackend):

    def __init__(self, expected_status, job_information):
        self._expected_status = expected_status
        self._job_information = job_information

    def get_paginated(self, start_index, number_to_get, status):
        if self._expected_status == status:
            return self._job_information

        return []
