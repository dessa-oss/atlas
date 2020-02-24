

from foundations_spec import *

class TestExecution(Spec):

    @let
    def translator(self):
        import foundations_internal.config.execution
        return foundations_internal.config.execution

    @let
    def _configuration(self):
        return {
            'results_config': {
                'archive_end_point': '',
            }
        }

    @let
    def _archive_types(self):
        return [
            'artifact_archive_implementation',
            'job_source_archive_implementation',
            'miscellaneous_archive_implementation',
            'persisted_data_archive_implementation',
            'provenance_archive_implementation',
        ]
    
    @let
    def fake_user(self):
        return self.faker.last_name()

    @let
    def fake_ip(self):
        return self.faker.ipv4()

    @let
    def fake_port(self):
        return self.faker.random_number()

    @let
    def fake_key_path(self):
        return self.faker.uri_path()
    
    @let
    def fake_artifact_path(self):
        return self.faker.uri_path()

    def test_returns_default_redis_url(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://localhost:6379')

    def test_returns_configured_redis_url(self):
        self._configuration['results_config']['redis_end_point'] = 'redis://11.22.33.44:9738'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://11.22.33.44:9738')

    def test_returns_run_script_environment_with_log_level_same_as_local_log_level(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['run_script_environment']['log_level'], 'DEBUG')

    def test_returns_run_script_environment_with_log_level_same_as_local_log_level_different_level(self):
        self._configuration['log_level'] = 'INFO'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['run_script_environment']['log_level'], 'INFO')

    def test_returns_log_level_configured_to_default(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'INFO')

    def test_returns_log_level_configured(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'DEBUG')

    def test_no_result_artifact_returns_constructor_arguments_with_default_artifact_path(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual('.', result_config['artifact_path'])

    def test_returns_archive_end_point(self):
        self._configuration['results_config']['archive_end_point'] = self.fake_artifact_path
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(self.fake_artifact_path, result_config['archive_end_point'])

    def test_validates_schema(self):
        import jsonschema

        bad_config = self.faker.pydict()
        with self.assertRaises(jsonschema.ValidationError) as error_context:
            self.translator.translate(bad_config)