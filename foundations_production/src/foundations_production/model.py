"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Model(object):
    
    def __init__(self, user_transformer_class, *args, **kwargs):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        from foundations_production.persister import Persister
        from foundations_production import model_package

        self._base_transformer = BaseTransformer(Preprocessor.active_preprocessor, Persister(model_package), user_transformer_class(*args, **kwargs))

    def fit(self, training_inputs, training_targets, validation_inputs, validation_targets):
        self._base_transformer.fit(training_inputs, training_targets, validation_inputs, validation_targets)

    def predict(self, inputs):
        return self._base_transformer.transformed_data(inputs)