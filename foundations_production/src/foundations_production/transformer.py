"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Transformer(object):
    
    def __init__(self, list_of_columns, user_transformer_class):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        from foundations_production.persister import Persister
        from foundations_production import model_package

        BaseTransformer(Preprocessor.active_preprocessor, Persister(model_package), user_transformer_class())

