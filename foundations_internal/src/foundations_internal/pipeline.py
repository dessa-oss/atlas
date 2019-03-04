"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.stage_context import StageContext


class Pipeline(object):

    def __init__(self, pipeline_context):
        self._pipeline_context = pipeline_context
        self._uuid = 'eecbbe4788acaee0393bcad40f37f134566ad8a7'

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._uuid

    def stage(self, function, *args, **kwargs):
        from foundations_internal.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.stage(self.uuid(), function, args, kwargs)
        builder = builder.hierarchy([self.uuid()])

        return builder.build()

    def run(self, **filler_kwargs):
        return None

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def persist(self):
        pass

    def require(self, *required_args):
        def _require(*args):
            pass

        return self.stage(_require, *required_args)
