"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.transformer import Transformer

class TestTransformer(Spec):

    base_transformer = let_patch_mock('foundations_production.base_transformer.BaseTransformer')
    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    persister_class = let_patch_mock('foundations_production.persister.Persister')
    global_model_package = let_patch_mock('foundations_production.model_package')
    user_transformer_class = let_mock()

    @let
    def fake_column_names(self):
        return self.faker.words()
    
    @let
    def user_transformer(self):
        return self.user_transformer_class.return_value
    
    @let
    def persister(self):
        return self.persister_class.return_value
          
    def test_transformer_constructs_persister_with_global_model_package(self):
        Transformer(self.fake_column_names, self.user_transformer_class)
        self.persister_class.assert_called_with(self.global_model_package)
    
    def test_transformer_constructs_base_transformer_with_correct_arguments(self):
        Transformer(self.fake_column_names, self.user_transformer_class)
        self.base_transformer.assert_called_with(self.global_preprocessor, self.persister, self.user_transformer)


