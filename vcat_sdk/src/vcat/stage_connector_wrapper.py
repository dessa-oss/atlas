"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_piping import StagePiping
from vcat.job import Job
from vcat.successive_argument_filler import SuccessiveArgumentFiller
from vcat.stage_connector import StageConnector
from vcat.stage_context import StageContext
from vcat.context_aware import ContextAware


class StageConnectorWrapper(object):

    def __init__(self, connector, pipeline_context, stage_context, stage_config):
        self._connector = connector
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context
        self._stage_config = stage_config

        self._stage_context.uuid = self.uuid()
        self._pipeline_context.add_stage_context(self._stage_context)

        self._stage_piping = StagePiping(self)

    def _reset_state(self):
        self._connector._reset_state()

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._connector.uuid()

    def add_tree_names(self, **filler_kwargs):
        self._connector.add_tree_names(
            self._pipeline_context.provenance.stage_hierarchy, self._provenance_filler_builder, **filler_kwargs)

    def stage(self, function, *args, **kwargs):
        from vcat.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.stage(self.uuid(), function, args, kwargs)
        builder = builder.hierarchy([self.uuid()])

        return builder.build(self._connector.stage)

    def persist(self):
        self._stage_config.persist()

    def set_global_cache_name(self, name):
        self._stage_config.cache(name)

    def enable_caching(self):
        self._stage_config.enable_caching()

    def disable_caching(self):
        self._stage_config.disable_caching()

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)

    def run(self, **filler_kwargs):
        self.add_tree_names(**filler_kwargs)
        return self.run_without_provenance(**filler_kwargs)

    def run_without_provenance(self, **filler_kwargs):
        return self._connector.run(self._filler_builder, **filler_kwargs)

    def _filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_fill import HyperparameterArgumentFill
        from vcat.stage_connector_wrapper_fill import StageConnectorWrapperFill

        return SuccessiveArgumentFiller([HyperparameterArgumentFill, StageConnectorWrapperFill], *args, **kwargs)

    def _provenance_filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_name_fill import HyperparameterArgumentNameFill
        from vcat.stage_connector_wrapper_name_fill import StageConnectorWrapperNameFill

        return SuccessiveArgumentFiller([HyperparameterArgumentNameFill, StageConnectorWrapperNameFill], *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def name(self):
        return self._connector.name()

    def splice(self, num_children):
        def splice_at(data_frames, slot_num):
            return data_frames[slot_num]

        children = []

        for child_index in range(num_children):
            child = self | (splice_at, child_index)
            children.append(child)

        return children

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, name):
        def call_method_on_instance(instance, *args, **kwargs):
            return getattr(instance, name)(*args, **kwargs)

        def auto_stage(*args, **kwargs):
            return self.stage(call_method_on_instance, *args, **kwargs)

        return auto_stage

    def __getitem__(self, key):
        def getitem(data):
            return data[key]

        return self.stage(getitem)

    def __setattr__(self, key, value):
        # self._connector = connector
        # self._pipeline_context = pipeline_context
        # self._stage_context = stage_context
        # self._stage_config = stage_config

        # self._stage_context.uuid = self.uuid()
        # self._pipeline_context.add_stage_context(self._stage_context)

        # self._stage_piping = StagePiping(self)


        if key in set(['_connector', '_pipeline_context', '_stage_context', '_stage_config', '_stage_config', '_stage_piping']):
            return super(StageConnectorWrapper, self).__setattr__(key, value)
        else:
            def setitem(data):
                data[key] = value
                return data

            return self.stage(setitem)