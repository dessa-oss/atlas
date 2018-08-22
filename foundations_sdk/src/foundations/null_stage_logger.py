"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class NullStageLogger(object):

    def log_metric(self, key, value):
        raise NotImplementedError()

    def pipeline_context(self):
        raise NotImplementedError()

    def stage(self):
        raise NotImplementedError()

    def stage_config(self):
        raise NotImplementedError()

    def stage_context(self):
        raise NotImplementedError()
