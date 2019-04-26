"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class Preprocessor(object):

    active_preprocessor = None

    def __init__(self, callback, preprocessor_name):
        self._transformers = []
        self._callback = callback
        self._is_inference_mode = False
        self._preprocessor_name = preprocessor_name

    def __call__(self, *args, **kwargs):
        import foundations

        self._transformers = []

        Preprocessor.active_preprocessor = self
        callback_value = self._callback(*args, **kwargs)

        if self._is_inference_mode:
            for transformer in self._transformers:
                transformer.load()

        self._is_inference_mode = True

        result = foundations.create_stage(self._serialize_callback)(callback_value)
        if isinstance(callback_value, tuple):
            result = result.split(len(callback_value))
        return result

    def _serialize_callback(self, args):
        from foundations_contrib.archiving import get_pipeline_archiver
        get_pipeline_archiver().append_artifact('preprocessor/' + self._preprocessor_name + '.pkl', self._callback)
        return args
    
    def new_transformer(self, transformer):
        self._transformers.append(transformer)
        transformer_index = len(self._transformers) - 1
        transformer_id = '{}_{}'.format(self._preprocessor_name, transformer_index)
        return transformer_id
    
    def set_inference_mode(self):
        self._is_inference_mode = True