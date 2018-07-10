"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class AdaptiveSearcher(object):
    def __init__(self, set_of_initial_params, params_generator_function, error_handler):
        from vcat.compat import make_queue
        from vcat.global_state import log_manager

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

        self._check_deployments_and_populate_queue(pipeline_to_run)

    def _add_results_to_list(self, deployment, jobs_done, all_logged_results):
        logged_results = deployment._try_get_results(self._error_handler)
        self._log.info(deployment.job_name() + ": " + str(logged_results))
        jobs_done.append(deployment.job_name())
        all_logged_results.append(logged_results)

    def _collect_results_and_remove_finished_deployments(self):
        from vcat.utils import _remove_items_by_key

        jobs_done = []
        all_logged_results = []

        for job_name, deployment in self._deployments_map.items():
            self._log.info(job_name + ": " + deployment.get_job_status())

            if deployment.is_job_complete():
                self._add_results_to_list(deployment, jobs_done, all_logged_results)

        _remove_items_by_key(self._deployments_map, jobs_done)

        self._log.info("----------\n")

        return all_logged_results

    def _check_deployments_and_populate_queue(self, pipeline_to_run):
        import time

        if self._deployments_map != {}:
            all_logged_results = self._collect_results_and_remove_finished_deployments()

            for logged_results in all_logged_results:
                new_params_sets = self._params_generator_function(logged_results)
                self._populate_queue(new_params_sets)

            if all_logged_results != []:
                self._drain_queue(pipeline_to_run)
            else:
                time.sleep(5)
                self._check_deployments_and_populate_queue(pipeline_to_run)
        else:
            self._log.info('Adaptive search completed.')

    def search(self, pipeline_to_run):
        self._drain_queue(pipeline_to_run)