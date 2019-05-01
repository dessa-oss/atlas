"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Transformer(object):
    
    def __init__(self, user_transformer_class, *args, **kwargs):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        import foundations

        user_stage = foundations.create_stage(user_transformer_class)(*args, **kwargs)
        self._base_transformer = BaseTransformer(Preprocessor.active_preprocessor, user_stage)

    def fit(self, data):
        self._base_transformer.fit(data)

    def transform(self, data):
        return self._base_transformer.transformed_data(data)
    
    def encoder(self):
        return self._base_transformer.encoder()
