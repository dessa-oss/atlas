"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class Scheduler(object):
    def __init__(self, scheduler_backend=None):
        self._backend = scheduler_backend

    def get_job_information(self, status=None):
        return self._backend.get_paginated(None, None, status)