"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.stage_connector_wrapper import StageConnectorWrapper
from foundations.discrete_hyperparameter import DiscreteHyperparameter
from foundations.deployment_wrapper import DeploymentWrapper

class DummyConnectorWrapper(StageConnectorWrapper):
    def __init__(self, *args, **kwargs):
        self.params_run = []

    def run(self, kwargs):
        self.params_run.append(kwargs)
        return DummyDeploymentWrapper(kwargs)

class DummyDeploymentWrapper(DeploymentWrapper):
    def __init__(self, data):
        import uuid

        self._job_name = str(uuid.uuid4())
        self._data = data

    def job_name(self):
        return self._job_name

    def fetch_job_results(self):
        import uuid
        return {
            'stage_contexts': {
                str(uuid.uuid4()): {
                    'stage_log': self._data
                }
            }
        }
    
    def is_job_complete(self):
        return True
    
    def get_job_status(self):
        return 'Completed'

def make_dummy_pipeline():
    return DummyConnectorWrapper()

simple_param_set = {'a': DiscreteHyperparameter([1])}

less_simple_param_set = {
    'a': DiscreteHyperparameter([1, 2])
}

params_ranges_dict = {
    'param_0': DiscreteHyperparameter([1, 2]),
    'param_1': DiscreteHyperparameter([3]),
    'param_2': DiscreteHyperparameter([4, 5, 6, 7])
}

def bad_params_generator(results):
    raise Exception

def dead_end(results):
    return []

def good_generator(results):
    if results['a'] + results['b'] < 5:
        return [{'a': results['a'] + 2, 'b': results['b'] + 1}, {'a': results['a'] + 1, 'b': results['b']}]
    else:
        return []