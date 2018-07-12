"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageConnectorWrapperBuilder(object):

    def __init__(self, graph, pipeline_context):
        from vcat.stage_context import StageContext
        from vcat.stage_config import StageConfig
        from vcat.middleware_chain import MiddlewareChain

        self._graph = graph
        self._pipeline_context = pipeline_context

        self._stage_context = StageContext()
        self._stage_config = StageConfig()

        self._middleware = MiddlewareChain()
        self._append_initial_middleware()

        self._stage = None
        self._connector = None

    def build(self, stage_function, *additional_args):
        from vcat.stage_connector_wrapper import StageConnectorWrapper

        connector = stage_function(self._stage, *additional_args)
        return StageConnectorWrapper(self._graph, connector, self._pipeline_context, self._stage_context, self._stage_config)

    def hierarchy(self, parent_uuids):
        stage_hierarchy = self._pipeline_context.provenance.stage_hierarchy
        stage_hierarchy.add_entry(self._stage, parent_uuids)

        return self

    def stage(self, current_uuid, function, args, kwargs):
        from vcat.stage import Stage

        stage_uuid = self._make_uuid(current_uuid, function, args, kwargs)
        self._stage_context.uuid = stage_uuid
        self._stage = Stage(self._middleware, stage_uuid,
                            function, function, *args, **kwargs)
        self._append_stage_middleware()
        return self

    def _append_initial_middleware(self):
        from vcat.global_state import middleware_manager

        for middleware in middleware_manager.initial_middleware():
            self._middleware.append_middleware(middleware.callback(self._stage_context))

    def _append_stage_middleware(self):
        from vcat.global_state import middleware_manager

        for middleware in middleware_manager.stage_middleware():
            self._middleware.append_middleware(middleware.callback(self._pipeline_context,
                                self._stage_config, self._stage_context, self._stage))

    def _uuid(self):
        return self._stage.uuid()

    def _make_uuid(self, current_uuid, function, args, kwargs):
        from vcat.argument_hasher import ArgumentHasher
        from vcat.utils import merged_uuids

        argument_hasher = ArgumentHasher(args, kwargs)
        argument_uuid = argument_hasher.make_hash()
        function_uuid = self._function_hash(function)
        return merged_uuids([current_uuid, function_uuid, argument_uuid])

    def _function_hash(self, function):
        from vcat.utils import generate_uuid
        from vcat.utils import merged_uuids
        from vcat.safe_inspect import getsource

        name_uuid = generate_uuid(function.__name__)
        source_uuid = generate_uuid(getsource(function))

        return merged_uuids([name_uuid, source_uuid])
