"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class Preprocessor(object):
    def __init__(self, callback):
        self._number_of_transformers = 0
        self._callback = callback

    def __call__(self, *args, **kwargs):
        Preprocessor.active_preprocessor = self
        return self._callback(*args, **kwargs)
    
    def new_transformer(self, transformer):
        self._number_of_transformers += 1
        return self._number_of_transformers - 1
