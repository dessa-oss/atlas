"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import foundations
from foundations_production.base_transformer import BaseTransformer


class ProductionModel(object):
    
    def __init__(self, job_id):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        import foundations

        self.job_id = job_id
        self._base_model = BaseTransformer(self, None)
        self._base_model.fit()
        self._base_model.load()

    def predict(self, *args, **kwargs):
        return self._base_model.transformed_data(*args, **kwargs)

    def new_transformer(self, transformer):
        return 'model_0'

    def encoder(self):
        return self._base_model.encoder()