"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SetSearcher(object):
    def __init__(self, params_set_generator, max_iterations):
        from vcat.utils import take_from_generator

        if max_iterations is None:
            self._params_set_generator = params_set_generator
        else:
            self._params_set_generator = take_from_generator(max_iterations, params_set_generator)

    def run_param_sets(self, pipeline_to_run):
        all_deployments = map(pipeline_to_run.run, self._params_set_generator)
        return {deployment.job_name(): deployment for deployment in all_deployments}