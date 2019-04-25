"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
from foundations_contrib.models.property_model import PropertyModel

class BaseTransformer(object):

    class State(PropertyModel):
        transformer_index = PropertyModel.define_property()
        persister = PropertyModel.define_property()
        should_load = PropertyModel.define_property()

    def __init__(self, preprocessor, persister, transformation):
        self._encoder = None
        self._transformation = transformation
        self._state = self.State(should_load=False, transformer_index=preprocessor.new_transformer(self), persister=persister)

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._fit_stage)(self._state, self._transformation, *args, **kwargs)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, *args, **kwargs):
        return foundations.create_stage(self._transformation_stage)(self.encoder(), *args, **kwargs)

    def load(self):
        self._state.should_load = True

    @staticmethod
    def _fit_stage(state, transformation, *args, **kwargs):
        if state.should_load:
            return BaseTransformer._loaded_transformer(state)
        return BaseTransformer._fitted_transformer(state, transformation, *args, **kwargs)

    @staticmethod
    def _fitted_transformer(state, transformation, *args, **kwargs):
        transformation.fit(*args, **kwargs)
        state.persister.save_transformation(state.transformer_index, transformation)
        return transformation

    @staticmethod
    def _loaded_transformer(state):
        return state.persister.load_transformation(state.transformer_index)

    @staticmethod
    def _transformation_stage(transformation, *args, **kwargs):
        return transformation.transform(*args, **kwargs)