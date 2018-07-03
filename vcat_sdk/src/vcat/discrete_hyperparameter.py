"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DiscreteHyperparameter(object):
    def __init__(self, values):
        self._values = values
    
    def grid_sample(self):
        for value in self._values:
            yield value

    def random_sample(self):
        import random

        if len(self._values) > 0:
            while True:
                yield random.choice(self._values)
        else:
            raise StopIteration