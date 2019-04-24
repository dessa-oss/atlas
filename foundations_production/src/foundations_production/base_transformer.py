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

    def fit(self, data):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._fit_stage)(data)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, data):
        return foundations.create_stage(self._transformation_stage)(data, self.encoder())

    def load(self):
        self._should_load = True

    def _fit_stage(self, data):
        if self._should_load:
            loaded_transformation = self._persister.load_transformation(self._transformer_index)
            return loaded_transformation
        self._transformation.fit(data)
        self._persister.save_transformation(self._transformer_index, self._transformation)
        return self._transformation

    @staticmethod
    def _transformation_stage(data, transformation):
        return transformation.transform(data)