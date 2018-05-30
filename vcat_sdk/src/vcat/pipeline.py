from vcat.stage_graph import StageGraph
from vcat.stage_piping import StagePiping
from vcat.stage_smart_constructor import StageSmartConstructor
from vcat.stage_connector_wrapper import StageConnectorWrapper
from vcat.stage_context import StageContext
from vcat.context_aware import ContextAware
from vcat.null_cache import NullCache
from vcat.utils import generate_uuid
from vcat.utils import merged_uuids


class Pipeline(object):

    def __init__(self, pipeline_context):
        self.graph = StageGraph()
        self.cache = NullCache()
        self.pipeline_context = pipeline_context
        self._stage_piping = StagePiping(self)
        self._uuid = generate_uuid('Humble beginnings...')

    def uuid(self):
        return self._uuid

    def stage(self, function, *args, **kwargs):
        new_context = StageContext()
        stage_smart_constructor = StageSmartConstructor(new_context)

        if isinstance(function, ContextAware):
            function._set_context(new_context)

        current_stage = stage_smart_constructor.make_stage(
            self.uuid(), new_context, function, *args, **kwargs)
        stage_hierarchy = self.pipeline_context.provenance.stage_hierarchy
        stage_hierarchy.add_entry(current_stage, [self.uuid()])
        return StageConnectorWrapper(self.graph.stage(self.cache, current_stage), self.pipeline_context, new_context)

    def join(self, upstream_connector_wrappers, function, *args, **kwargs):
        upstream_connectors = [
            wrapper._connector for wrapper in upstream_connector_wrappers]
        upstream_uuids = [connector.uuid()
                          for connector in upstream_connectors]

        current_uuid = merged_uuids(upstream_uuids)
        parent_uuids = upstream_uuids
        new_context = StageContext()
        stage_smart_constructor = StageSmartConstructor(new_context)
        current_stage = stage_smart_constructor.make_stage(
            current_uuid, new_context, function, *args, **kwargs)
        stage_hierarchy = self.pipeline_context.provenance.stage_hierarchy
        stage_hierarchy.add_entry(current_stage, parent_uuids)
        return StageConnectorWrapper(self.graph.join(self.cache, current_stage, upstream_connectors), self.pipeline_context, new_context)

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)
