"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DeploymentWrapper(object):
    def __init__(self, deployment):
        self._job_name = deployment.job_name()
        self._is_job_complete = deployment.is_job_complete()
        self._complete_checked = 0

    def job_name(self):
        return self._job_name

    def is_job_complete(self):
        if self._complete_checked == 0:
            self._complete_checked += 1
            return self._is_job_complete
        else:
            return True