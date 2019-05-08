"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from foundations_production.preprocessor_class import Preprocessor

def callback_function(*args, **kwargs):
    return args, kwargs

class MockTransformerClass(object):
    def __init__(self):
        self.loaded = False
        self.load_call_count = 0

    def load(self):
        self.loaded = True
        self.load_call_count+=1

class MockClass(object):
    def __call__(self, *args):
        if args:
            return args[0] + 5

class TestPreprocessorClass(Spec):

    mock_transformer = let_mock()
    mock_transformer_2 = let_mock()

    mock_pipeline_archiver = let_mock()

    @let_now
    def mock_archiver(self):
        instance = Mock()
        callback = self.patch('foundations_production.preprocessor_class.get_pipeline_archiver_for_job', ConditionalReturn())
        callback.return_when(instance, self.job_id)
        return instance

    @let_now
    def foundations_context(self):
        from foundations_internal.foundations_context import FoundationsContext
        mock_current_foundations_context = self.patch('foundations_production.preprocessor_class.current_foundations_context')
        mock_current_foundations_context.return_value = FoundationsContext(self.pipeline) 
        return mock_current_foundations_context

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
    
    @let
    def mock_class(self):
        return MockClass()
    
    @let
    def serialized_mock_class(self):
        from foundations_internal.serializer import serialize
        return serialize(self.mock_class)
    
    @let
    def serialized_callback_function(self):
        from foundations_internal.serializer import serialize
        return serialize(callback_function)

    @let
    def fake_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.preprocessor_instance = Preprocessor(callback_function, self.preprocessor_name)
        self.mock_pipeline_archiver.fetch_artifact = ConditionalReturn()
        self.mock_pipeline_archiver.fetch_artifact.return_when(self.serialized_mock_class, 'preprocessor/{}.pkl'.format(self.fake_name))

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
        self.assertEqual(self.random_number, self.preprocessor_instance(self.random_number)[0][0].run_same_process())
    
    def test_preprocessor_calls_callback_when_called_and_supports_tuple_return(self):
        expected_result = tuple(self.faker.words())
        result = tuple(stage.run_same_process() for stage in self.preprocessor_instance(expected_result))
        self.assertEqual(expected_result, result[0][0])
    
    def test_preprocessor_calls_callback_with_arguments_and_keyword_arguments_when_called(self):
        result = tuple(stage.run_same_process() for stage in self.preprocessor_instance('gorilla', banana='yellow'))
        self.assertEqual( (('gorilla',), {'banana':'yellow'}), result)

    def test_new_transformer_returns_transformer_index_of_0_when_first_transformer_added(self):
        transformer = MockTransformerClass()
        transformer_id = self.preprocessor_instance.new_transformer(transformer)
        self.assertEqual('{}_0'.format(self.preprocessor_name), transformer_id)
    
    def test_new_transformer_returns_correct_transformer_index_when_transformer_added(self):
        transformer = MockTransformerClass()
        for _ in range(self.random_number):
            transformer_id = self.preprocessor_instance.new_transformer(transformer)
        self.assertEqual('{}_{}'.format(self.preprocessor_name, self.random_number - 1), transformer_id)

    def test_preprocessor_loads_transformer_if_inference_mode_is_set(self):
        transformer = MockTransformerClass()
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()

        self.assertTrue(transformer.loaded)
    
    def test_preprocessor_does_not_double_track_transformers_if_preprocessor_called_twice(self):
        transformer = MockTransformerClass()

        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(2, transformer.load_call_count)

    def test_preprocessor_is_set_to_inference_mode_after_being_run(self):
        transformer = MockTransformerClass()
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance()
        preprocessor_instance()

        self.assertEqual(1, transformer.load_call_count)

    def test_preprocessor_loads_transformers_if_inference_mode_is_set(self):
        transformer_0 = MockTransformerClass()
        transformer_1 = MockTransformerClass()

        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer_0)
            Preprocessor.active_preprocessor.new_transformer(transformer_1)
       
        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        result = preprocessor_instance()
        self.assertTrue(transformer_0.loaded)
        self.assertTrue(transformer_1.loaded)

    def test_preprocessor_does_not_load_transformer_if_inference_mode_is_not_set(self):
        transformer = MockTransformerClass()
        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance()

        self.assertFalse(transformer.loaded)

    def test_preprocessor_saves_callback_when_returned_stage_is_executed(self):
        stage = self.preprocessor_instance()[0]
        stage.run_same_process()
        self.mock_archiver.append_artifact.assert_called_with('preprocessor/' + self.preprocessor_name + '.pkl', self.serialized_callback_function)

    def test_preprocessor_saves_callback_when_instantiated(self):
        self.preprocessor_instance()
        self.mock_archiver.append_artifact.assert_not_called()

    def test_job_id_is_a_stage_that_returns_the_current_job_id(self):
        job_id_stage = self.preprocessor_instance.job_id
        self.assertEqual(self.job_id, job_id_stage.run_same_process())

    def test_job_id_is_the_value_of_the_job_id_when_one_is_provided(self):
        preprocessor = Preprocessor(callback_function, self.preprocessor_name, job_id=self.job_id)
        job_id_stage = preprocessor.job_id
        self.assertEqual(self.job_id, job_id_stage.run_same_process())
    
    def test_get_inference_mode_gets_inference_mode_false_by_default(self):
        self.assertFalse(self.preprocessor_instance.get_inference_mode())
    
    def test_get_inference_mode_gets_inference_mode_true_when_set(self):
        self.preprocessor_instance.set_inference_mode()
        self.assertTrue(self.preprocessor_instance.get_inference_mode())

    def test_load_preprocessor_loads_transformer_preprocessor(self):
        preprocessor = Preprocessor.load_preprocessor(self.mock_pipeline_archiver, self.fake_name, self.job_id)
        actual_value = preprocessor(self.random_number)
        self.assertEqual(self.random_number+5, actual_value.run_same_process())

    def test_load_preprocessor_loads_transformer_preprocessor_with_correct_name(self):
        preprocessor = Preprocessor.load_preprocessor(self.mock_pipeline_archiver, self.fake_name, self.job_id)
        preprocessor(self.random_number)
        new_transformer_index = preprocessor.new_transformer(None)
        self.assertEqual('{}_0'.format(self.fake_name), new_transformer_index)

    def test_load_preprocessor_loads_transformer_preprocessor_with_job_id(self):
        preprocessor = Preprocessor.load_preprocessor(self.mock_pipeline_archiver, self.fake_name, self.job_id)
        preprocessor(self.random_number)
        self.assertEqual(self.job_id, preprocessor.job_id.run_same_process())
    
    def test_transformer_preprocessor_inference_mode_is_true(self):
        preprocessor = Preprocessor.load_preprocessor(self.mock_pipeline_archiver, self.fake_name, self.job_id)
        self.assertTrue(preprocessor.get_inference_mode())

    def test_inference_mode_false_when_inference_mode_set_to_false(self):
        preprocessor = Preprocessor.load_preprocessor(self.mock_pipeline_archiver, self.fake_name, self.job_id)
        preprocessor.set_inference_mode(inference_mode=False)

        self.assertFalse(preprocessor.get_inference_mode())

    def test_preprocessor_does_not_load_loaded_transformer_when_inference_mode_false(self):
        transformer = MockTransformerClass()

        def _callback():
            Preprocessor.active_preprocessor.new_transformer(transformer)

        preprocessor_instance = Preprocessor(_callback, self.preprocessor_name)
        preprocessor_instance.set_inference_mode()
        preprocessor_instance()
        preprocessor_instance.set_inference_mode(inference_mode=False)
        preprocessor_instance()

        self.assertEqual(1, transformer.load_call_count)