"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.transformer_saver import TransformerSaver

class TestTransformerSaver(Spec):
    
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
    def transformer_saver(self):
        return TransformerSaver(self.job_id)

    @let_now
    def mock_get_pipeline_archiver(self):
        mock_get_pipeline_archiver = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock_get_pipeline_archiver.return_when(self.mock_pipeline_archiver, self.job_id)
        return mock_get_pipeline_archiver

    def test_transformer_saver_saves_serialized_transformer_to_model_package(self):
        self.transformer_saver.save_user_defined_transformer(self.transformer_id, self.transformer)
        self.mock_pipeline_archiver.append_artifact.assert_called_with(self.transformer_artifact_name, self.transformer)
