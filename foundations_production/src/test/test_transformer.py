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
    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    persister_class = let_patch_mock('foundations_production.persister.Persister')
    global_model_package = let_patch_mock('foundations_production.model_package')
    user_transformer_class = let_mock()

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
    def base_transformer(self):
        return self.base_transformer_class.return_value

    @let
    def persister(self):
        return self.persister_class.return_value
          
    def test_transformer_constructs_persister_with_global_model_package(self):
        Transformer(self.user_transformer_class, self.fake_column_names)
        self.persister_class.assert_called_with(self.global_model_package)
    
    def test_transformer_constructs_base_transformer_with_correct_arguments(self):
        Transformer(self.user_transformer_class, self.fake_column_names)
        self.base_transformer_class.assert_called_with(self.global_preprocessor, self.persister, self.user_transformer)
    
    def test_fit_fits_selected_columns(self):
        from pandas.testing import assert_frame_equal

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class, selected_columns)
        transformer.fit(self.fake_data)

        sliced_dataframe = self.base_transformer.fit.call_args[0][0]
        assert_frame_equal(self.fake_data[selected_columns], sliced_dataframe)
    
    def test_fit_fits_all_columns_when_none_provided(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class)
        transformer.fit(self.fake_data)

        sliced_dataframe = self.base_transformer.fit.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)
    
    def test_transform_transforms_selected_columns(self):
        from pandas.testing import assert_frame_equal

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class, selected_columns)
        transformer.transform(self.fake_data)

        sliced_dataframe = self.base_transformer.transformed_data.call_args[0][0]
        assert_frame_equal(self.fake_data[selected_columns], sliced_dataframe)

    def test_transform_returns_all_transformed_data_when_no_columns_specified(self):
        from pandas.testing import assert_frame_equal

        transformer = Transformer(self.user_transformer_class)
        transformer.transform(self.fake_data)

        sliced_dataframe = self.base_transformer.transformed_data.call_args[0][0]
        assert_frame_equal(self.fake_data, sliced_dataframe)        

    def test_transform_returns_transformed_selected_columns(self):
        from pandas.testing import assert_frame_equal

        self.base_transformer.transformed_data.return_value = self.fake_transformed_data

        selected_columns = self.fake_column_names[0:2]

        transformer = Transformer(self.user_transformer_class, selected_columns)
        joined_data = transformer.transform(self.fake_data)

        assert_frame_equal(self.fake_transformed_data, joined_data)

    def test_user_transformer_constructs_with_arbitrary_arguments(self):
        args = self.faker.words()
        kwargs = self.faker.pydict()

        transformer = Transformer(self.user_transformer_class, self.fake_column_names, *args, **kwargs)

        self.user_transformer_class.assert_called_with(*args, **kwargs)


