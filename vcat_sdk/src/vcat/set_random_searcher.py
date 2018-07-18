"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.set_searcher import SetSearcher

class SetRandomSearcher(SetSearcher):
    def __init__(self, params_range_dict, max_iterations):
        params_set_generator = SetRandomSearcher._create_random_params_set_generator(params_range_dict)
        super(SetRandomSearcher, self).__init__(params_set_generator, max_iterations)

    @staticmethod
    def _generate_random_params_set(params_range_dict):
        return {key: params_range.random_sample() for key, params_range in params_range_dict.items()}

    @staticmethod
    def _create_random_params_set_generator(params_range_dict):
        while True:
            yield SetRandomSearcher._generate_random_params_set(params_range_dict)