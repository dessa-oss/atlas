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

        def fit_stage(self, user_defined_transformer, *args, **kwargs):
            if self.should_load:
                return self._loaded_transformer()
            return self._fitted_transformer(user_defined_transformer, *args, **kwargs)
        
        def _loaded_transformer(self):
            return self.persister.load_user_defined_transformer(self.transformer_index)

        def _fitted_transformer(self, user_defined_transformer, *args, **kwargs):
            user_defined_transformer.fit(*args, **kwargs)
            self.persister.save_user_defined_transformer(self.transformer_index, user_defined_transformer)
            return user_defined_transformer

    def __init__(self, preprocessor, persister, user_defined_transformer):
        self._encoder = None
        self._user_defined_transformer = user_defined_transformer
        self._state = self.State(should_load=False, transformer_index=preprocessor.new_transformer(self), persister=persister)

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._state.fit_stage)(self._user_defined_transformer, *args, **kwargs)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, *args, **kwargs):
        return foundations.create_stage(self._user_defined_transformer_stage)(self.encoder(), *args, **kwargs)

    def load(self):
        self._state.should_load = True

    @staticmethod
    def _user_defined_transformer_stage(user_defined_transformer, *args, **kwargs):
        return user_defined_transformer.transform(*args, **kwargs)