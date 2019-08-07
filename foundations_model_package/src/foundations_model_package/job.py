"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Job(object):
    
    def __init__(self, environment):
        self._environment = environment

    def id(self):
        return self._id()

    def root(self):
        return f'/archive/archive/{self._id()}/artifacts'

    def _id(self):
        return self._environment['JOB_ID']