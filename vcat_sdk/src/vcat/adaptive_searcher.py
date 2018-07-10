"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class AdaptiveSearcher(object):
    def __init__(self, set_of_initial_params, params_generator_function, error_handler):
        from vcat.compat import make_queue

        self._params_queue = make_queue()
        self._deployments_map = {}

        self._params_generator_function = params_generator_function
        self._error_handler = error_handler

        self._populate_queue(set_of_initial_params)

    def _populate_queue(self, set_of_initial_params):
        for initial_params in set_of_initial_params:
            self._params_queue.put(initial_params)

    def _drain_queue(self, pipeline_to_run):
        from vcat.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self._params_queue.empty():
            params_to_run = self._params_queue.get()
            deployment = pipeline_to_run.run(params_to_run)
            self._deployments_map[deployment.job_name()] = deployment
            log.info(deployment.job_name() + ' created')

        log.info('----------\n')

        self._check_deployments_and_populate_queue(pipeline_to_run)

    def _check_deployments_and_populate_queue(self, pipeline_to_run):
        import time

        from vcat.global_state import log_manager
        from vcat.deployment_utils import _collect_results_and_remove_finished_deployments

        log = log_manager.get_logger(__name__)

        if self._deployments_map != {}:
            all_logged_results = _collect_results_and_remove_finished_deployments(self._deployments_map, self._error_handler)

            for logged_results in all_logged_results:
                new_params_sets = self._params_generator_function(logged_results)
                self._populate_queue(new_params_sets)

            if all_logged_results != []:
                self._drain_queue(pipeline_to_run)
            else:
                time.sleep(5)
                self._check_deployments_and_populate_queue(pipeline_to_run)
        else:
            log.info('Adaptive search completed.')

    def search(self, pipeline_to_run):
        self._drain_queue(pipeline_to_run)