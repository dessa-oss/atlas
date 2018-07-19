"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DiscreteHyperparameter(object):
    """Holds an internal list of possible values for hyperparameter substitution.
        Arguments:
            values: {list} -- The list of values to use for hyperparameter substitution
    """

    def __init__(self, values):
        self._values = list(values)
    
    def grid_elements(self):
        """Retrieve the internal list of values intended for use in grid search.
        
        Returns:
            values -- The list of values over which to iterate for grid search
        """
        return self._values

    def random_sample(self):
        """Randomly choose a single element for use in random search.

        Returns:
            value -- A single, randomly-chosen value for use in random search
        """
        import random

        if len(self._values) > 0:
            return random.choice(self._values)
        else:
            raise ValueError("cannot sample from empty list")