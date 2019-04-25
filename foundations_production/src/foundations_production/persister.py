"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Persister(object):
    
    def __init__(self, archiver):
        self._archiver = archiver

    def load_user_defined_transformer(self, transformer_id):
        pass

    def save_user_defined_transformer(self, transformer_id, transformer):
        self._archiver.append_artifact('preprocessor/' + transformer_id, transformer)