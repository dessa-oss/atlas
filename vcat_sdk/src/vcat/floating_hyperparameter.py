"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FloatingHyperparameter(object):
    """Helper object used for an analogue of range() for floats in the case of grid search,
        and a uniform distribution in the case of random search.

        Arguments:
            min: {float} -- Left end of uniform distribution
            max: {float} -- Right end of uniform distribution
            step: {float} -- Grid size for grid search - think range(min, max, step), where max is actually included.
    """

    def __init__(self, min, max, step):
        self._min = min
        self._max = max
        self._step = step

        self._values = None

    def grid_elements(self):
        """Create list of values intended for use in grid search - similar to range.
        
        Returns:
            values -- The list of values over which to iterate for grid search
        """
        if self._values is None:
            self._values = []
            current = self._min

            while(current <= self._max):
                self._values.append(current)
                current += self._step

        return self._values

    def random_sample(self):
        """Randomly choose an element for use in random search (uniformly distributed).  Step is ignored.

        Returns:
            value -- A single, randomly-chosen value for use in random search
        """
        import random

        return random.uniform(self._min, self._max)