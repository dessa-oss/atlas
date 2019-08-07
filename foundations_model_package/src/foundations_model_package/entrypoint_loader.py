"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class EntrypointLoader(object):
    
    def __init__(self, job):
        self._job = job

    def entrypoint_function(self):
        raise Exception(f'Job {self._job.id()} not found!')