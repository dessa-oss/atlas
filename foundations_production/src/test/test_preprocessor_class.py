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

    mock_archiver = let_patch_instance('foundations_production.preprocessor_class.get_pipeline_archiver')

    @let_now
    def foundations_context(self):
        from foundations_internal.foundations_context import FoundationsContext
        return self.patch('foundations_production.preprocessor_class.foundations_context', FoundationsContext(self.pipeline))

    @let_now
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @let_now
    def pipeline(self):
        from foundations_internal.pipeline import Pipeline
        return Pipeline(self.pipeline_context)

    @set_up
    def set_up_foundations_context(self):
        self.pipeline_context.file_name = self.job_id

    @let
    def job_id(self):
        return self.faker.sha1()

    @let
    def random_number(self):
        import random
        return random.randint(1, 10)
    
    @let
    def preprocessor_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.preprocessor_instance = Preprocessor(self.mock_callback, self.preprocessor_name)

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
        self.assertEqual(self.random_number, self.preprocessor_instance().run_same_process())
    
    def test_preprocessor_calls_callback_when_called_and_supports_tuple_return(self):
        expected_result = tuple(self.faker.words())
        self.mock_callback.return_value = expected_result
        result = tuple(stage.run_same_process() for stage in self.preprocessor_instance())
        self.assertEqual(expected_result, result)
    
    def test_preprocessor_calls_callback_with_arguments_when_called(self):
        self.mock_callback.return_value = self.random_number
        self.preprocessor_instance('gorilla', banana='yellow')
        self.mock_callback.assert_called_with('gorilla', banana='yellow')

    def test_new_transformer_returns_transformer_index_of_0_when_first_transformer_added(self):
        transformer_id = self.preprocessor_instance.new_transformer(self.mock_transformer)
        self.assertEqual('{}_0'.format(self.preprocessor_name), transformer_id)
    
    def test_new_transformer_returns_correct_transformer_index_when_transformer_added(self):
        for _ in range(self.random_number):
            transformer_id = self.preprocessor_instance.new_transformer(self.mock_transformer)
        self.assertEqual('{}_{}'.format(self.preprocessor_name, self.random_number - 1), transformer_id)

    def test_preprocessor_loads_transformer_if_inference_mode_is_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()

        self.mock_transformer.load.assert_called()
    
    def test_preprocessor_does_not_double_track_transformers_if_preprocessor_called_twice(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(2, self.mock_transformer.load.call_count)

    def test_preprocessor_is_set_to_inference_mode_after_being_run(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(1, self.mock_transformer.load.call_count)

    def test_preprocessor_loads_transformers_if_inference_mode_is_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer_2)
       
        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()

        self.mock_transformer.load.assert_called()
        self.mock_transformer_2.load.assert_called()

    def test_preprocessor_does_not_load_transformer_if_inference_mode_is_not_set(self):
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(self.mock_transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance()

        self.mock_transformer.load.assert_not_called()

    def test_preprocessor_saves_callback_when_returned_stage_is_executed(self):
        stage = self.preprocessor_instance()
        stage.run_same_process()
        self.mock_archiver.append_artifact.assert_called_with('preprocessor/' + self.preprocessor_name + '.pkl', self.mock_callback)

    def test_preprocessor_saves_callback_when_instantiated(self):
        self.preprocessor_instance()
        self.mock_archiver.append_artifact.assert_not_called()

    def test_job_id_is_a_stage_that_returns_the_current_job_id(self):
        job_id_stage = self.preprocessor_instance.job_id
        self.assertEqual(self.job_id, job_id_stage.run_same_process())

    def test_job_id_is_the_value_of_the_job_id_when_one_is_provided(self):
        preprocessor = Preprocessor(self.mock_callback, self.preprocessor_name, job_id=self.job_id)
        job_id_stage = preprocessor.job_id
        self.assertEqual(self.job_id, job_id_stage.run_same_process())
    
    def test_get_inference_mode_gets_inference_mode_false_by_default(self):
        self.assertFalse(self.preprocessor_instance.get_inference_mode())
    
    def test_get_inference_mode_gets_inference_mode_true_when_set(self):
        self.preprocessor_instance.set_inference_mode()
        self.assertTrue(self.preprocessor_instance.get_inference_mode())