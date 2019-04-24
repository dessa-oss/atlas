"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations


class BaseTransformer(object):

    def __init__(self, preprocessor, transformation):
        self._encoder = None
        self._transformation = transformation
        preprocessor.new_transformer(self)

    def fit(self, data):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._fit_stage)(data, self._transformation)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, data):
        return foundations.create_stage(self._transformation_stage)(data, self.encoder())

    @staticmethod
    def _transformation_stage(data, transformation):
        return transformation.transform(data)

    @staticmethod
    def _fit_stage(data, transformation):
        transformation.fit(data)
        return transformation