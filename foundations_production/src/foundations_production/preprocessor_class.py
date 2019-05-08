"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_contrib.archiving import get_pipeline_archiver_for_job
from foundations_contrib.global_state import current_foundations_context
from foundations import create_stage

class Preprocessor(object):

    active_preprocessor = None

    def __init__(self, callback, preprocessor_name, job_id=None):
        import foundations

        self._transformers = []
        self._callback = callback
        self._is_inference_mode = False
        self._preprocessor_name = preprocessor_name

        self.job_id = foundations.create_stage(self._job_id_stage)(job_id)

    def __call__(self, *args, **kwargs):
        self._transformers = []

        Preprocessor.active_preprocessor = self
        callback_value = self._callback(*args, **kwargs)

        if self._is_inference_mode:
            for transformer in self._transformers:
                transformer.load()

        self._is_inference_mode = True

        return self._serialization_stage(callback_value)

    @staticmethod
    def _job_id_stage(job_id):
        if job_id is None:
            return current_foundations_context().job_id()
        else:
            return job_id

    def  _serialization_stage(self, callback_value):
        from foundations_internal.serializer import serialize

        serialized_callback = serialize(self._callback)
        result = create_stage(self._serialize_callback)(self._preprocessor_name, serialized_callback, callback_value)

        if isinstance(callback_value, tuple):
            result = result.split(len(callback_value))
        return result

    @staticmethod
    def _serialize_callback(preprocessor_name, callback, args):
        job_id = current_foundations_context().job_id()
        get_pipeline_archiver_for_job(job_id).append_artifact('preprocessor/' + preprocessor_name + '.pkl', callback)
        return args

    def new_transformer(self, transformer):
        self._transformers.append(transformer)
        transformer_index = len(self._transformers) - 1
        transformer_id = '{}_{}'.format(self._preprocessor_name, transformer_index)
        return transformer_id
    
    def set_inference_mode(self, inference_mode=True):
        self._is_inference_mode = inference_mode
    
    def get_inference_mode(self):
        return self._is_inference_mode

    @staticmethod
    def load_preprocessor(pipeline_archiver, preprocessor_name, job_id):
        from foundations_internal.serializer import deserialize

        serialized_preprocessor_callback = pipeline_archiver.fetch_artifact('preprocessor/{}.pkl'.format(preprocessor_name))
        preprocessor_callback = deserialize(serialized_preprocessor_callback)
        preprocessor = Preprocessor(preprocessor_callback, preprocessor_name, job_id)
        preprocessor.set_inference_mode()
        return preprocessor
