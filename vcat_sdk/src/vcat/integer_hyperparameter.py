"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.discrete_hyperparameter import DiscreteHyperparameter

class IntegerHyperparameter(DiscreteHyperparameter):
    """Represents a range of integer values for use in hyperparameter substitution.

        Arguments:
            start: {int} -- The start of the range of values (defaults to 0)
            stop: {int} -- The end of the range of values (exclusive)
            step: {int} -- The number to increment by (defaults to 1)
    """

    def __init__(self, *args, **kwargs):
        super(IntegerHyperparameter, self).__init__(range(*args, **kwargs))