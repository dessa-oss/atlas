"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import foundations
from foundations_production.persister import Persister
from foundations_production.transformer_saver import TransformerSaver

class BaseTransformer(object):

    class State(object):

        def __init__(self, transformer_index):
            self.should_load = False
            self.should_retrain = False
            self.transformer_index = transformer_index
             
        def fit_stage(self, persister, user_defined_transformer, *args, **kwargs):
            transformer_saver_for_currently_executing_job = self._transformer_saver_for_currently_executing_job()

            if self.should_load:
                loaded_transformer = self._loaded_transformer(persister)

                if self.should_retrain:
                    self._fit_transformer(transformer_saver_for_currently_executing_job, loaded_transformer, *args, **kwargs)

                return loaded_transformer

            self._fit_transformer(transformer_saver_for_currently_executing_job, user_defined_transformer, *args, **kwargs)
            return user_defined_transformer
        
        def _loaded_transformer(self, persister):
            return persister.load_user_defined_transformer(self.transformer_index)

        def _fit_transformer(self, persister, user_defined_transformer, *args, **kwargs):
            user_defined_transformer.fit(*args, **kwargs)
            persister.save_user_defined_transformer(self.transformer_index, user_defined_transformer)
    
        @staticmethod
        def _transformer_saver_for_currently_executing_job():
            from foundations_contrib.global_state import current_foundations_context
            current_job_id = current_foundations_context().job_id()
            return TransformerSaver(current_job_id)

    def __init__(self, preprocessor, user_defined_transformer):
        self._encoder = None
        self._user_defined_transformer = user_defined_transformer

        self._persister_stage = foundations.create_stage(self._create_persister)(job_id=preprocessor.job_id)
        self._state = self.State(transformer_index=preprocessor.new_transformer(self))

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._state.fit_stage)(self._persister_stage, self._user_defined_transformer, *args, **kwargs)

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
    def _create_persister(job_id):
        return Persister(job_id)

    @staticmethod
    def _user_defined_transformer_stage(user_defined_transformer, *args, **kwargs):
        if hasattr(user_defined_transformer, 'predict'):
            return user_defined_transformer.predict(*args, **kwargs)
        return user_defined_transformer.transform(*args, **kwargs)