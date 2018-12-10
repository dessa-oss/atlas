"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class AdaptiveSearcher(object):
    def __init__(self, set_of_initial_params, params_generator_function, error_handler):
        from foundations_internal.compat import make_queue
        from foundations.global_state import log_manager

        self._params_queue = make_queue()
        self._deployments_map = {}

        self._params_generator_function = params_generator_function
        self._error_handler = error_handler
        self._log = log_manager.get_logger(__name__)

        self._populate_queue(set_of_initial_params)

    def _populate_queue(self, set_of_initial_params):
        for initial_params in set_of_initial_params:
            self._params_queue.put(initial_params)

    def _drain_queue(self, pipeline_to_run):
        while not self._params_queue.empty():
            params_to_run = self._params_queue.get()
            deployment = pipeline_to_run.run(params_to_run)
            self._deployments_map[deployment.job_name()] = deployment
            self._log.info(deployment.job_name() + ' created')

        self._log.info('----------\n')

    def _collect_results_and_remove_finished_deployments(self):
        from foundations.deployment_utils import collect_results_and_remove_finished_deployments

        return collect_results_and_remove_finished_deployments(self._log, self._deployments_map, self._error_handler)

    def _check_deployments_and_populate_queue(self):
        import time

        all_logged_results = self._collect_results_and_remove_finished_deployments()

        for logged_results in all_logged_results:
            new_params_sets = self._params_generator_function(logged_results)
            self._populate_queue(new_params_sets)

        return all_logged_results

    def _is_search_done(self):
        return self._deployments_map == {} and self._params_queue.empty()

    def search(self, pipeline_to_run):
        import time

        STATE_DRAINING = "DRAINING"
        STATE_POPULATING = "POPULATING"

        current_state = STATE_DRAINING

        while not self._is_search_done():
            if current_state == STATE_DRAINING:
                self._drain_queue(pipeline_to_run)
                current_state = STATE_POPULATING
            elif current_state == STATE_POPULATING:
                all_logged_results = self._check_deployments_and_populate_queue()

                if all_logged_results != []:
                    current_state = STATE_DRAINING
                else:
                    time.sleep(5)
            else:
                raise ValueError("unknown state: " + current_state)

        self._log.info('Adaptive search completed.')
