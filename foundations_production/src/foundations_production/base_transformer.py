"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations


class BaseTransformer(object):

    def __init__(self, preprocessor, persister, transformation):
        self._encoder = None
        self._transformation = transformation
        self._persister = persister
        self._transformer_index = preprocessor.new_transformer(self)
        self._should_load = False

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._fit_stage)(*args, **kwargs)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, *args, **kwargs):
        return foundations.create_stage(self._transformation_stage)(self.encoder(), *args, **kwargs)

    def load(self):
        self._should_load = True

    def _fit_stage(self, *args, **kwargs):
        if self._should_load:
            return self._loaded_transformer()
        return self._fitted_transformer(*args, **kwargs)

    def _fitted_transformer(self, *args, **kwargs):
        self._transformation.fit(*args, **kwargs)
        self._persister.save_transformation(self._transformer_index, self._transformation)
        return self._transformation

    def _loaded_transformer(self):
        return self._persister.load_transformation(self._transformer_index)

    @staticmethod
    def _transformation_stage(transformation, *args, **kwargs):
        return transformation.transform(*args, **kwargs)