"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Job(object):

    def __init__(self, pipeline_connector, **kwargs):
        self.kwargs = kwargs
        self._pipeline_connector = pipeline_connector

    def run(self):
        self._pipeline_connector.pipeline_context().provenance.job_run_data = self.kwargs
        return self._pipeline_connector.run_same_process(**self.kwargs)

    def pipeline_context(self):
        return self._pipeline_connector.pipeline_context()

    def serialize(self):
        from foundations.serializer import serialize
        return serialize(self)

    @staticmethod
    def deserialize(serialized_self):
        from foundations.serializer import deserialize
        return deserialize(serialized_self)
