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

    def run(self, params_dict={}, **kw_params):
        import uuid

        from vcat.global_state import deployment_manager
        from vcat.deployment_wrapper import DeploymentWrapper

        all_params = params_dict.copy()
        all_params.update(kw_params)

        job_name = str(uuid.uuid4())
        job = Job(self, **all_params)
        deployment = deployment_manager.deploy({}, job_name, job)

        return DeploymentWrapper(deployment)

    def run_same_process(self, **filler_kwargs):
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
        if name.startswith('__') and name.endswith('__'):
            return super(StageConnectorWrapper, self).__getattr__(name)

        def call_method_on_instance(instance, *args, **kwargs):
            result = getattr(instance, name)(*args, **kwargs)
            if result is None:
                return instance

        def auto_stage(*args, **kwargs):
            return self.stage(call_method_on_instance, *args, **kwargs)

        return auto_stage

    def __getitem__(self, key):
        def getitem(data, key):
            return data[key]

        return self.stage(getitem, key)

    @staticmethod
    def _generate_random_params_set(params_range_dict):
        params_set = {}

        for key, params_range in params_range_dict.items():
            params_set[key] = params_range.random_sample()

        return params_set

    @staticmethod
    def _create_random_params_set_generator(params_range_dict, max_iterations):
        for _ in range(max_iterations):
            yield StageConnectorWrapper._generate_random_params_set()

    def _create_and_run_param_sets(self, params_set_generator):
        all_deployments = map(self.run, params_set_generator)
        return all_deployments

    def random_search(self, params_range_dict, max_iterations):
        random_params_set_generator = StageConnectorWrapper._create_random_params_set_generator(params_range_dict, max_iterations)
        return self._create_and_run_param_sets(random_params_set_generator)

    @staticmethod
    def _lazily_generate_all_grid_search_params(params_range_dict):
        

    @staticmethod
    def _generate_grid_search_params(params_range_dict, max_iterations):
        from vcat.utils import take_from_generator

        all_params_set_generator = StageConnectorWrapper._lazily_generate_all_grid_search_params(params_range_dict)
        
        if max_iterations is None:
            return all_params_set_generator
        else:
            return take_from_generator(max_iterations, all_params_set_generator)

    def grid_search(self, params_range_dict, max_iterations=None):
        grid_params_set_generator = StageConnectorWrapper._generate_grid_search_params(params_range_dict, max_iterations)
        return self._create_and_run_param_sets(grid_params_set_generator)

    # def adaptive_search(self, set_of_initial_params, params_generator, n_iterations=None):
    #     import Queue
    #     import uuid

    #     from vcat.deployment_utils import _extract_results

    #     queue = Queue.Queue()

    #     for initial_params in set_of_initial_params:
    #         queue.put(initial_params)

    #     while not queue.empty():
    #         self._reset_state()

    #         param_set = queue.get()
    #         deployment = self.run(param_set)

    #         for new_params in generator_function(_extract_results(results_dict)):
    #             queue.put(new_params)
