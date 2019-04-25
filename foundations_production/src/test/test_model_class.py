"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.model_class import Model

class TestModel(Spec):

    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    artifact_archive = let_mock()
    foundations_context = let_patch_mock('foundations_contrib.global_state.foundations_context')
    pipeline_archiver = let_mock()
    artifact_archive = let_mock()

    @let_now
    def job_id(self):
        job_id = self.faker.uuid4()
        self.foundations_context.job_id.return_value = job_id
        return job_id
    
    @let_now
    def load_archive(self):
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(self.artifact_archive, 'artifact_archive')
        return load_archive
    
    @let_now
    def pipeline_archiver_class(self):
        pipeline_archiver_class = self.patch('foundations_internal.pipeline_archiver.PipelineArchiver', ConditionalReturn())
        pipeline_archiver_class.return_when(self.pipeline_archiver, self.job_id, None, None, None, None, None, self.artifact_archive, None)
        return pipeline_archiver_class

    @let
    def transformer_args(self):
        return self.faker.words()

    @let
    def transformer_kwargs(self):
        return self.faker.pydict()

    user_transformer = let_mock()
    
    @let_now
    def user_transformer_class(self):
        klass = ConditionalReturn()
        klass.return_when(self.user_transformer, *self.transformer_args, **self.transformer_kwargs)
        return klass

    @let_now
    def persister(self):
        instance = Mock()
        klass = self.patch('foundations_production.persister.Persister', ConditionalReturn())
        klass.return_when(instance, self.pipeline_archiver)
        return instance

    fake_training_inputs = let_mock()
    fake_training_targets = let_mock()
    fake_validation_inputs = let_mock()
    fake_validation_targets = let_mock()

    @let_now
    def base_transformer(self):
        instance = Mock()

        def _base_transformer_constructor(preprocessor, persister, user_defined_transformer_stage):
            self.assertEqual(self.global_preprocessor, preprocessor)
            self.assertEqual(self.persister, persister)
            self.assertEqual(self.user_transformer, user_defined_transformer_stage.run_same_process())
            return instance

        klass = self.patch('foundations_production.base_transformer.BaseTransformer')
        klass.side_effect = _base_transformer_constructor
        return instance

    @let_now
    def mock_transform(self):
        self.base_transformer.transformed_data = ConditionalReturn()
        return self.base_transformer.transformed_data

    @let
    def transformer(self):
        return Model(self.user_transformer_class_callback, *self.transformer_args, **self.transformer_kwargs)

    @set_up
    def set_up(self):
        self.mock_transform.return_when(self.fake_validation_targets, self.fake_validation_inputs)

    def user_transformer_class_callback(self, *args, **kwargs):
        return self.user_transformer_class(*args, **kwargs)
          
    def test_fit_fits_selected_columns(self):
        self.transformer.fit(
            self.fake_training_inputs, 
            self.fake_training_targets, 
            self.fake_validation_inputs, 
            self.fake_validation_targets
        )

        self.base_transformer.fit.assert_called_with(
            self.fake_training_inputs, 
            self.fake_training_targets, 
            self.fake_validation_inputs, 
            self.fake_validation_targets
        )
    
    def test_transform_transforms_selected_columns(self):
        self.assertEqual(self.fake_validation_targets, self.transformer.predict(self.fake_validation_inputs))
