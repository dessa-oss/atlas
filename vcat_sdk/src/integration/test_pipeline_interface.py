import unittest


class TestPipelineInterface(unittest.TestCase):
    def test_simple_callback(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        
        self.assertEqual(staged_stages.make_data().run(), stages.make_data())

    def test_simple_callback_with_params(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        
        self.assertEqual(staged_stages.make_data('hello').run(), stages.make_data('hello'))

    def test_simple_callback_with_hyper_params(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        from vcat import Hyperparameter
        
        self.assertEqual(staged_stages.make_data(Hyperparameter('data')).run(data='world'), stages.make_data('world'))

    def test_simple_callback_with_named_params(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        from vcat import Hyperparameter
        
        self.assertEqual(staged_stages.make_data(data='potato').run(), stages.make_data('potato'))

    def test_simple_callback_with_staged_params(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        from vcat import Hyperparameter
        
        previous_stage = staged_stages.make_data('world')
        self.assertEqual(staged_stages.make_data(previous_stage).run(), stages.make_data('world'))

    def test_simple_callback_with_multiple_staged_params(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages
        from vcat import Hyperparameter
        
        previous_stage = staged_stages.make_data('hello ')
        previous_stage_two = staged_stages.make_data('world')
        self.assertEqual(staged_stages.concat_data(previous_stage, previous_stage_two).run(), stages.concat_data('hello ', 'world'))

    def test_import_external_library(self):
        from staged_json import dumps

        self.assertEqual(dumps({'a': 4.5}).run(), '{"a": 4.5}')