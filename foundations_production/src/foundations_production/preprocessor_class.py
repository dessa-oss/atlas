"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class Preprocessor(object):
    def __init__(self):
        self._number_of_transformers = 0

    def __call__(self):
        Preprocessor.active_preprocessor = self
    
    def new_transformer(self, transformer):
        self._number_of_transformers += 1
        return self._number_of_transformers - 1
