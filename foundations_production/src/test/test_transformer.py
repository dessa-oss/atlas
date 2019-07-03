"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.transformer import Transformer

class TestTransformer(Spec):

    base_transformer_class = let_patch_mock('foundations_production.base_transformer.BaseTransformer')
    base_transformer = let_mock()
    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    user_transformer_class = let_mock()
    foundations_context = let_patch_mock('foundations_contrib.global_state.foundations_context')
    pipeline_archiver = let_mock()
    artifact_archive = let_mock()
    
    @let
    def job_id(self):
        return self.faker.uuid4()

    @let_now
    def load_archive(self):
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(self.artifact_archive, 'artifact_archive')
        return load_archive

    @let_now
    def pipeline_archiver_class(self):
        return self.patch('foundations_internal.pipeline_archiver.PipelineArchiver', ConditionalReturn())

    def user_transformer_class_callback(self, *args, **kwargs):
        return self.user_transformer_class(*args, **kwargs)

    @let
    def fake_column_names(self):
        return self.faker.words(3)
    
    @let
    def fake_data(self):
        import pandas

        return pandas.DataFrame({
            self.fake_column_names[0]: [self.random_int],
            self.fake_column_names[1]: [self.random_int],
            self.fake_column_names[2]: [self.random_int]
        })

    @let
    def random_int(self):
        return self.faker.random_int()

    @let
    def different_random_int(self):
        return self.faker.random_int()

    @let
    def fake_transformed_data(self):
        import pandas

        return pandas.DataFrame({
            self.fake_column_names[0]: [self.different_random_int],
            self.fake_column_names[1]: [self.different_random_int]
        })

    @let
    def user_transformer(self):
        return self.user_transformer_class.return_value

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        config_manager = ConfigManager()
        config_manager['run_script_environment'] = {'enable_stages': True}
        return self.patch('foundations.config_manager', config_manager)

    @set_up
    def set_up(self):
        def _base_transformer_constructor(preprocessor, user_defined_transformer_stage):
            user_defined_transformer_stage.run_same_process()
            return self.base_transformer

        self.base_transformer_class.side_effect = _base_transformer_constructor
        
        self.foundations_context.job_id.return_value = self.job_id
        self.pipeline_archiver_class.return_when(self.pipeline_archiver, self.job_id, None, None, None, None, None, self.artifact_archive, None)
          
    def test_transformer_constructs_base_transformer_with_correct_arguments(self):
        def _base_transformer_constructor(preprocessor, user_defined_transformer_stage):
            self.assertEqual(self.global_preprocessor, preprocessor)
            self.assertEqual(self.user_transformer, user_defined_transformer_stage.run_same_process())

        self.base_transformer_class.side_effect = _base_transformer_constructor
        Transformer(self.user_transformer_class_callback)
    
    
    def test_fit_fits_all_columns(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class_callback)
        transformer.fit(self.fake_data)

        sliced_dataframe = self.base_transformer.fit.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)
    
    def test_transform_transforms_all_data(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class_callback)
        transformer.transform(self.fake_data)

        sliced_dataframe = self.base_transformer.transformed_data.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)

    def test_user_transformer_constructs_with_arbitrary_arguments(self):
        args = self.faker.words()
        kwargs = self.faker.pydict()

        transformer = Transformer(self.user_transformer_class_callback, *args, **kwargs)

        self.user_transformer_class.assert_called_with(*args, **kwargs)

    def test_user_transformer_constructs_with_single_argument_and_no_columns(self):
        arg = self.faker.word()

        transformer = Transformer(self.user_transformer_class_callback, arg)

        self.user_transformer_class.assert_called_with(arg)
    
    def test_encoder_returns_encoder(self):
        transformer = Transformer(self.user_transformer_class_callback)
        self.assertEqual(self.base_transformer.encoder(), transformer.encoder())

