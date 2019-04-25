"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Persister(object):
    
    def __init__(self, model_package):
        self._model_package = model_package

    def load_user_defined_transformer(self, transformer_id):
        pass

    def save_user_defined_transformer(self, transformer_id, transformer):
        from foundations_internal.serializer import serialize

        self._model_package.save_serialized_transformer(serialize(1))