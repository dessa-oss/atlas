"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_contrib.global_state import foundations_context


class Model(object):
    
    def __init__(self, user_model_class, *args, **kwargs):
        from foundations import create_stage
        from foundations_production.base_transformer import BaseTransformer

        user_stage = create_stage(user_model_class)(*args, **kwargs)
        
        self.job_id = create_stage(self._job_id_stage)()
        self._base_model = BaseTransformer(self, user_stage)

    @staticmethod
    def _job_id_stage():
        return foundations_context.job_id()

    def fit(self, *args, **kwargs):
        self._base_model.fit(*args, **kwargs)
        return self._base_model.encoder()

    def predict(self, *args, **kwargs):
        return self._base_model.transformed_data(*args, **kwargs)

    def new_transformer(self, transformer):
        return 'model_0'
