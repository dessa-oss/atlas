"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Model(object):
    
    def __init__(self, user_model_class, *args, **kwargs):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        from foundations_production.persister import Persister
        import foundations

        persister = Persister(self._get_artifact_archive())
        user_stage = foundations.create_stage(user_model_class)(*args, **kwargs)
        self._base_model = BaseTransformer(Preprocessor.active_preprocessor, persister, user_stage)

    def fit(self, training_inputs, training_targets, validation_inputs, validation_targets):
        self._base_model.fit(training_inputs, training_targets, validation_inputs, validation_targets)

    def predict(self, inputs):
        return self._base_model.transformed_data(inputs)

    @staticmethod
    def _get_artifact_archive():
        from foundations import config_manager
        config = config_manager.config()
        return config['artifact_archive_implementation']