"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class Preprocessor(object):
    def __init__(self, callback):
        self._transformers = []
        self._callback = callback

    def __call__(self, *args, **kwargs):
        Preprocessor.active_preprocessor = self
        callback_value = self._callback(*args, **kwargs)
        for transformer in self._transformers:
            transformer.load()
        return callback_value
    
    def new_transformer(self, transformer):
        self._transformers.append(transformer)
        return len(self._transformers) - 1
    
    def set_inference_mode(self):
        pass
