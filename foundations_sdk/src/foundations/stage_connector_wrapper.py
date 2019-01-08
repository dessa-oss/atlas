"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.job import Job
from foundations_internal.stage_context import StageContext
from foundations.context_aware import ContextAware


class StageConnectorWrapper(object):
    """
    ### The three numerals at the begining are a marker for not generating user documentation for the class.
    """

    def __init__(self, stage, pipeline_context, stage_context, stage_config):
        self._stage = stage
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context
        self._stage_config = stage_config

        self._stage_context.uuid = self.uuid()
        self._pipeline_context.add_stage_context(self._stage_context)

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._stage.uuid()

    def stage(self, function, *args, **kwargs):
        from foundations import foundations_context

        return foundations_context.pipeline().stage(function, self, *args, **kwargs)

    def require(self, *required_args):
        def _require(*args):
            return args[-1]

        builder = self._make_builder()
        builder = self._set_builder_stage(
            builder, _require, required_args + (self,), {})
        builder = self._set_builder_hierarchy(builder)

        return builder.build(self._stage)

    def persist(self):
        self._stage_config.persist()
        return self

    def set_global_cache_name(self, name):
        self._stage_config.cache(name)
        return self

    def enable_caching(self):
        """
        Activates caching of all input parameters for this stage.

        Arguments:
            - This method doesn't receive any argument

        Returns:
            stage object -- The same object to which this method belongs.

        Raises:
            - This method normally doesn't raise exceptions.

        Notes:
            At this moment only input parameters that are return values of other stages are cached.
        """
        self._stage_config.enable_caching()
        for argument in self._stage.stage_args():
            argument.enable_caching()
        for argument in self._stage.stage_kwargs().values():
            argument.enable_caching()
        return self

    def disable_caching(self):
        self._stage_config.disable_caching()
        return self

    def run(self, params_dict=None, job_name=None, **kw_params):
        """
        Deploys and runs the current stage and the stages on which it depends in the configured execution
        environment, creating a new job.

        Arguments:
            params_dict {dictionary} -- optional dictionary of extra parameters to pass the job that would be created.
            job_name {string} -- optional name for the job that would be created.
            kw_params {keyword arguments} -- any other optional paramater to pass to the job.

        Returns:
            deployment {DeploymentWrapper} -- An object that allows tracking the deployment.

        Raises:
            TypeError -- When an unsupported type is passed to a user function

        Notes
            The new job runs asynchronously, the current process can continue execution.
        """
        from foundations.global_state import deployment_manager
        from foundations.deployment_wrapper import DeploymentWrapper
        from foundations import log_manager

        if params_dict is None:
            params_dict = {}

        all_params = params_dict.copy()
        all_params.update(kw_params)

        logger = log_manager.get_logger(__name__)

        logger.info("Deploying job...")
        deployment = deployment_manager.simple_deploy(
            self, job_name, all_params)
        deployment_wrapper = DeploymentWrapper(deployment)

        return deployment_wrapper

    def run_same_process(self, **filler_kwargs):
        return self._stage.run(None, None, **filler_kwargs)

    def _make_builder(self):
        from foundations_internal.stage_connector_wrapper_builder import StageConnectorWrapperBuilder
        return StageConnectorWrapperBuilder(self._pipeline_context)

    def _set_builder_stage(self, builder, function, args, kwargs):
        return builder.stage(self.uuid(), function, args, kwargs)

    def _set_builder_hierarchy(self, builder):
        return builder.hierarchy([self.uuid()])

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def name(self):
        function_name_and_uuid = self.function_name() + ' ' + self.uuid()
        return function_name_and_uuid

    def function_name(self):
        return self._stage.function_name()

    def split(self, num_children):
        """
        When a function is wrapped in a stage and it has more than one return value (the return value
        is a sequence), the wrapping stage cannot obtain how many values are contained in the returned
        sequence due to language contrains. This method allows to specify the number of children values
        and splits the result in a corresponding sequence of stages that can be pass forward.

        Arguments:
            num_children {int} -- number of children values contained in the stage result.

        Returns:
            children_stages {sequence} -- A sequence of children stages.

        Raises:
            TypeError -- If the current stage does not contain a sequence of values.
            IndexError -- If the number of children values is less than __num_children__.
        """
        from foundations.utils import split_at

        children = []

        for child_index in range(num_children):
            child = self.stage(split_at, child_index)
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
