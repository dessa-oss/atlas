"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class CompletedJob(object):
    
    def __init__(self, job_id=None, user=None, input_params=None, output_metrics=None, status=None):
        self._job_id = job_id
        self._user = user
        self._input_params = input_params
        self._output_metrics = output_metrics
        self._status = status

    @property
    def job_id(self):
        return self._job_id

    @property
    def user(self):
        return self._user

    @property
    def input_params(self):
        return self._input_params

    @property
    def output_metrics(self):
        return self._output_metrics

    @property
    def status(self):
        return self._status