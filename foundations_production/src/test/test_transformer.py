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
    persister_class = let_patch_mock('foundations_production.persister.Persister')
    global_model_package = let_patch_mock('foundations_production.model_package')
    user_transformer_class = let_mock()

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
    
    @let
    def persister(self):
        return self.persister_class.return_value

    @set_up
    def set_up(self):
        def _base_transformer_constructor(preprocessor, persister, user_defined_transformer_stage):
            user_defined_transformer_stage.run_same_process()
            return self.base_transformer

        self.base_transformer_class.side_effect = _base_transformer_constructor
          
    def test_transformer_constructs_persister_with_global_model_package(self):
        Transformer(self.user_transformer_class_callback, self.fake_column_names)
        self.persister_class.assert_called_with(self.global_model_package)
    
    def test_transformer_constructs_base_transformer_with_correct_arguments(self):
        def _base_transformer_constructor(preprocessor, persister, user_defined_transformer_stage):
            self.assertEqual(self.global_preprocessor, preprocessor)
            self.assertEqual(self.persister, persister)
            self.assertEqual(self.user_transformer, user_defined_transformer_stage.run_same_process())

        self.base_transformer_class.side_effect = _base_transformer_constructor
        Transformer(self.user_transformer_class_callback, self.fake_column_names)
    
    def test_fit_fits_selected_columns(self):
        from pandas.testing import assert_frame_equal

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class_callback, list_of_columns=selected_columns)
        transformer.fit(self.fake_data)

        sliced_dataframe = self.base_transformer.fit.call_args[0][0]
        assert_frame_equal(self.fake_data[selected_columns], sliced_dataframe)
    
    def test_fit_fits_all_columns_when_none_provided(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class_callback)
        transformer.fit(self.fake_data)

        sliced_dataframe = self.base_transformer.fit.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)
    
    def test_transform_transforms_selected_columns(self):
        from pandas.testing import assert_frame_equal

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class_callback, list_of_columns=selected_columns)
        transformer.transform(self.fake_data)

        sliced_dataframe = self.base_transformer.transformed_data.call_args[0][0]
        assert_frame_equal(self.fake_data[selected_columns], sliced_dataframe)

    def test_transform_returns_all_transformed_data_when_no_columns_specified(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class_callback)
        transformer.transform(self.fake_data)

        sliced_dataframe = self.base_transformer.transformed_data.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)        

    def test_transform_returns_transformed_selected_columns(self):
        from pandas.testing import assert_frame_equal

        self.base_transformer.transformed_data.return_value = self.fake_transformed_data

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class_callback, list_of_columns=selected_columns)
        joined_data = transformer.transform(self.fake_data)

        assert_frame_equal(self.fake_transformed_data, joined_data)

    def test_user_transformer_constructs_with_arbitrary_arguments(self):
        args = self.faker.words()
        kwargs = self.faker.pydict()

        transformer = Transformer(self.user_transformer_class_callback, list_of_columns=self.fake_column_names, *args, **kwargs)

        self.user_transformer_class.assert_called_with(*args, **kwargs)

    def test_user_transformer_constructs_with_single_arguement_and_no_columns(self):
        arg = self.faker.word()

        transformer = Transformer(self.user_transformer_class_callback, arg)

        self.user_transformer_class.assert_called_with(arg)


