
from foundations_spec import *
from foundations.local_run.initialize_default_environment import create_config_file

class TestInitializeDefaultEnvironment(Spec):

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_mkdirs = let_patch_mock('os.makedirs')
    mock_typed_config_klass = let_patch_mock_with_conditional_return('foundations_core_cli.typed_config_listing.TypedConfigListing')
    mock_typed_config = let_mock()

    @let
    def mock_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda *_: mock_file
        mock_file.__exit__ = Mock()
        mock_file.write = self._write_file_data
        return mock_file

    @set_up
    def set_up(self):
        self.mock_open.return_when(self.mock_file, 'config/execution/default.config.yaml', 'w+')
        self.mock_typed_config_klass.return_when(self.mock_typed_config, 'execution')
        self.mock_typed_config.config_path = ConditionalReturn()
        self.mock_typed_config.config_path.return_when(None, 'default')
        self._file_data = None

    def test_create_default_config_creates_default_execution_config(self):
        import yaml

        create_config_file()
        config = yaml.load(self._file_data)
        self.assertEqual({'results_config': {}, 'cache_config': {}}, config)

    def test_create_default_does_not_create_config_if_already_existing(self):
        import yaml

        self.mock_typed_config.config_path.clear()
        self.mock_typed_config.config_path.return_when('config/execution/default.config.yaml', 'default')
        self._file_data = "---\nhello: world\n"

        create_config_file()
        config = yaml.load(self._file_data)
        self.assertEqual({'hello': 'world'}, config)

    def test_ensure_directory_exists(self):
        create_config_file()
        self.mock_mkdirs.assert_called_with('config/execution', exist_ok=True)

    def _write_file_data(self, data):
        self._file_data = data

