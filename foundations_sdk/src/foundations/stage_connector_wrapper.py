"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.stage_piping import StagePiping
from foundations.job import Job
from foundations.successive_argument_filler import SuccessiveArgumentFiller
from foundations.stage_connector import StageConnector
from foundations.stage_context import StageContext
from foundations.context_aware import ContextAware


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
        builder = self._make_builder()
        builder = self._set_builder_stage(builder, function, args, kwargs)
        builder = self._set_builder_hierarchy(builder)

        return builder.build(self._connector.stage)

    def require(self, *required_args):
        def _require(*args):
            return args[-1]

        builder = self._make_builder()
        builder = self._set_builder_stage(
            builder, _require, required_args + (self,), {})
        builder = self._set_builder_hierarchy(builder)

        return builder.build(self._connector.stage)

    def persist(self):
        self._stage_config.persist()
        return self

    def set_global_cache_name(self, name):
        self._stage_config.cache(name)
        return self

    def enable_caching(self):
        self._stage_config.enable_caching()
        for argument in self._connector.args():
            argument.enable_caching()
        for argument in self._connector.kwargs().values():
            argument.enable_caching()
        return self

    def disable_caching(self):
        self._stage_config.disable_caching()
        return self

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)

    def run(self, params_dict=None, job_name=None, **kw_params):
        from foundations.global_state import deployment_manager
        from foundations.deployment_wrapper import DeploymentWrapper

        if params_dict is None:
            params_dict = {}

        all_params = params_dict.copy()
        all_params.update(kw_params)

        deployment = deployment_manager.simple_deploy(self, job_name, all_params)

        return DeploymentWrapper(deployment)

    def run_same_process(self, **filler_kwargs):
        self.add_tree_names(**filler_kwargs)
        return self.run_without_provenance(**filler_kwargs)

    def run_without_provenance(self, **filler_kwargs):
        return self._connector.run(self._filler_builder, **filler_kwargs)

    def _make_builder(self):
        from foundations.stage_connector_wrapper_builder import StageConnectorWrapperBuilder
        return StageConnectorWrapperBuilder(self._pipeline_context)

    def _set_builder_stage(self, builder, function, args, kwargs):
        return builder.stage(self.uuid(), function, args, kwargs)

    def _set_builder_hierarchy(self, builder):
        return builder.hierarchy([self.uuid()])

    def _filler_builder(self, *args, **kwargs):
        from foundations.hyperparameter_argument_fill import HyperparameterArgumentFill
        from foundations.stage_connector_wrapper_fill import StageConnectorWrapperFill

        return SuccessiveArgumentFiller([HyperparameterArgumentFill, StageConnectorWrapperFill], *args, **kwargs)

    def _provenance_filler_builder(self, *args, **kwargs):
        from foundations.hyperparameter_argument_name_fill import HyperparameterArgumentNameFill
        from foundations.stage_connector_wrapper_name_fill import StageConnectorWrapperNameFill

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
        if name.startswith('__') and name.endswith('__'):
            return super(StageConnectorWrapper, self).__getattr__(name)

        def call_method_on_instance(instance, *args, **kwargs):
            result = getattr(instance, name)(*args, **kwargs)
            if result is None:
                return instance
            return result

        def auto_stage(*args, **kwargs):
            return self.stage(call_method_on_instance, *args, **kwargs)

        return auto_stage

    def __getitem__(self, key):
        def getitem(data, key):
            return data[key]

        return self.stage(getitem, key)

    def random_search(self, params_range_dict, max_iterations):
        from foundations.set_random_searcher import SetRandomSearcher

        set_random_searcher = SetRandomSearcher(
            params_range_dict, max_iterations)
        return set_random_searcher.run_param_sets(self)

    def grid_search(self, params_range_dict, max_iterations=None):
        from foundations.set_grid_searcher import SetGridSearcher

        grid_searcher = SetGridSearcher(params_range_dict, max_iterations)
        return grid_searcher.run_param_sets(self)

    def adaptive_search(self, set_of_initial_params, params_generator_function, error_handler=None):
        from foundations.adaptive_searcher import AdaptiveSearcher

        adaptive_searcher = AdaptiveSearcher(
            set_of_initial_params, params_generator_function, error_handler)
        adaptive_searcher.search(self)
