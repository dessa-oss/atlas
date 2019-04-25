"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.persister import Persister

class TestPersister(Spec):
    
    mock_serialize = let_patch_mock('foundations_internal.serializer.serialize')
    model_package = let_mock()
    user_defined_transformer = let_mock()

    @let
    def transformer_index(self):
        return self.faker.random_int()

    @let
    def serialized_transformer(self):
        return self.faker.sentence()

    def test_save_transformer_saves_serialized_transformer_to_model_package(self):
        self.mock_serialize.return_value = self.serialized_transformer

        persister = Persister(self.model_package)
        persister.save_user_defined_transformer(self.transformer_index, self.user_defined_transformer)

        self.model_package.save_serialized_transformer.assert_called_with(self.serialized_transformer)