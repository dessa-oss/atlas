"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.transformer_loader import TransformerLoader

class TestTransformerLoader(Spec):
    
    transformer = let_mock()
    mock_pipeline_archiver = let_mock()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def transformer_id(self):
        return '{}_{}'.format(self.faker.word(), self.faker.random_int())

    @let
    def transformer_artifact_name(self):
        return 'preprocessor/' + self.transformer_id

    @let
    def transformer_loader(self):
        return TransformerLoader(self.job_id)

    @let_now
    def mock_get_pipeline_archiver(self):
        mock_get_pipeline_archiver = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock_get_pipeline_archiver.return_when(self.mock_pipeline_archiver, self.job_id)
        return mock_get_pipeline_archiver

    def test_transformer_loader_loads_serialized_transformer_from_model_package(self):
        self.mock_pipeline_archiver.fetch_artifact = ConditionalReturn()
        self.mock_pipeline_archiver.fetch_artifact.return_when(self.transformer, self.transformer_artifact_name)
        loaded_transformer = self.transformer_loader.load_user_defined_transformer(self.transformer_id)
        self.assertEqual(self.transformer, loaded_transformer)
