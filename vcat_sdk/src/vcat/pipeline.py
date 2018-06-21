"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_graph import StageGraph
from vcat.stage_piping import StagePiping
from vcat.stage_connector_wrapper import StageConnectorWrapper
from vcat.stage_context import StageContext
from vcat.context_aware import ContextAware
from vcat.utils import generate_uuid
from vcat.utils import merged_uuids


class Pipeline(object):

    def __init__(self, pipeline_context):
        self.graph = StageGraph()
        self._pipeline_context = pipeline_context
        self._stage_piping = StagePiping(self)
        self._uuid = generate_uuid('Humble beginnings...')

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._uuid

    def stage(self, function, *args, **kwargs):
        from vcat.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.stage(self.uuid(), function, args, kwargs)
        builder = builder.hierarchy([self.uuid()])

        return builder.build(self.graph.stage)

    def join(self, upstream_connector_wrappers, function, *args, **kwargs):
        from vcat.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        upstream_connectors = [
            wrapper._connector for wrapper in upstream_connector_wrappers]
        upstream_uuids = [connector.uuid()
                          for connector in upstream_connectors]
        current_uuid = merged_uuids(upstream_uuids)

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.stage(current_uuid, function, args, kwargs)
        builder = builder.hierarchy(upstream_uuids)

        return builder.build(self.graph.join, upstream_connectors)

    def run(self, **filler_kwargs):
        return None

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def persist(self):
        pass

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)
