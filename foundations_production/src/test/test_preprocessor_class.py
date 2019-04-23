"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from foundations_production.preprocessor_class import Preprocessor

class TestPreprocessorClass(Spec):

    mock_transformer = let_mock()
    mock_transformer_2 = let_mock()

    mock_callback = let_mock()

    @let
    def random_number(self):
        import random
        return random.randint(1, 10)
    
    @set_up
    def set_up(self):
        self.preprocessor_instance = Preprocessor(self.mock_callback)

    @tear_down
    def tear_down(self):
        try:
            getattr(Preprocessor, 'active_preprocessor')
            Preprocessor.active_preprocessor = None
        except AttributeError:
            pass

    def test_preprocessor_sets_active_preprocessor_to_itself_when_called(self):
        self.preprocessor_instance()
        self.assertIs(self.preprocessor_instance, Preprocessor.active_preprocessor)

    def test_preprocessor_active_preprocessor_is_none_by_default(self):
        self.assertIsNone(Preprocessor.active_preprocessor)

    def test_preprocessor_calls_callback_when_called(self):
        self.mock_callback.return_value = self.random_number
        self.assertEqual(self.random_number, self.preprocessor_instance())
    
    def test_preprocessor_calls_callback_with_arguments_when_called(self):
        self.mock_callback.return_value = self.random_number
        self.preprocessor_instance('gorilla', banana='yellow')
        self.mock_callback.assert_called_with('gorilla', banana='yellow')

    def test_new_transformer_returns_transformer_index_of_0_when_first_transformer_added(self):
        transformer_id = self.preprocessor_instance.new_transformer(self.mock_transformer)
        self.assertEqual(0, transformer_id)
    
    def test_new_transformer_returns_correct_transformer_index_when_transformer_added(self):
        for _ in range(self.random_number):
            transformer_id = self.preprocessor_instance.new_transformer(self.mock_transformer)
        self.assertEqual(self.random_number - 1, transformer_id)

    def test_preprocessor_loads_transformer_if_inference_mode_is_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()

        self.mock_transformer.load.assert_called()
    
    def test_preprocessor_does_not_double_track_transformers_if_preprocessor_called_twice(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(2, self.mock_transformer.load.call_count)

    def test_preprocessor_is_set_to_inference_mode_after_being_run(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback)
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(1, self.mock_transformer.load.call_count)

    def test_preprocessor_loads_transformers_if_inference_mode_is_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer_2)

        preprocessor_instance = Preprocessor(_callback)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()

        self.mock_transformer.load.assert_called()
        self.mock_transformer_2.load.assert_called()

    def test_preprocessor_does_not_load_transformer_if_inference_mode_is_not_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback)
        preprocessor_instance()

        self.mock_transformer.load.assert_not_called()