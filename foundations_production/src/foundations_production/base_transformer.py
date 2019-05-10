"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import foundations
from foundations_production.transformer_saver import TransformerSaver
from foundations_production.transformer_loader import TransformerLoader
from foundations_contrib.global_state import current_foundations_context

class BaseTransformer(object):

    class State(object):

        def __init__(self, transformer_index):
            self.should_load = False
            self.should_retrain = False
            self.transformer_index = transformer_index
             
        def fit_stage(self, transformer_loader, transformer_saver, user_defined_transformer, *args, **kwargs):
            if self.should_load:
                loaded_transformer = self._loaded_transformer(transformer_loader)

                if self.should_retrain:
                    self._fit_transformer(transformer_saver, loaded_transformer, *args, **kwargs)

                return loaded_transformer

            self._fit_transformer(transformer_saver, user_defined_transformer, *args, **kwargs)
            return user_defined_transformer
        
        def _loaded_transformer(self, transformer_loader):
            return transformer_loader.load_user_defined_transformer(self.transformer_index)

        def _fit_transformer(self, transformer_saver, user_defined_transformer, *args, **kwargs):
            user_defined_transformer.fit(*args, **kwargs)
            transformer_saver.save_user_defined_transformer(self.transformer_index, user_defined_transformer)

    def __init__(self, preprocessor, user_defined_transformer):
        self._encoder = None
        self._user_defined_transformer = user_defined_transformer

        id_of_job_to_run = foundations.create_stage(self._get_id_of_job_to_run)()

        self._transformer_saver_stage = foundations.create_stage(self._create_transformer_saver)(job_id=id_of_job_to_run)
        self._transformer_loader_stage = foundations.create_stage(self._create_transformer_loader)(job_id=preprocessor.job_id)
        self._state = self.State(transformer_index=preprocessor.new_transformer(self))

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._state.fit_stage)(self._transformer_loader_stage, self._transformer_saver_stage, self._user_defined_transformer, *args, **kwargs)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, *args, **kwargs):
        return foundations.create_stage(self._user_defined_transformer_stage)(self.encoder(), *args, **kwargs)

    def load(self):
        self._state.should_load = True

    def prepare_for_retrain(self):
        self._state.should_retrain = True
        self._encoder = None
        
    @staticmethod
    def _create_transformer_loader(job_id):
        return TransformerLoader(job_id)

    @staticmethod
    def _create_transformer_saver(job_id):
        return TransformerSaver(job_id)

    @staticmethod
    def _get_id_of_job_to_run():
        return current_foundations_context().job_id()

    @staticmethod
    def _user_defined_transformer_stage(user_defined_transformer, *args, **kwargs):
        if hasattr(user_defined_transformer, 'predict'):
            return user_defined_transformer.predict(*args, **kwargs)
        return user_defined_transformer.transform(*args, **kwargs)