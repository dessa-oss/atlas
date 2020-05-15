
from foundations_spec import *
from mock import patch

import foundations.utils as utils

class MockModule(object):
    def __init__(self, file_path):
        self.__file__ = file_path

class TestUtils(Spec):

    mock_logger = let_mock()

    @set_up
    def set_up(self):
        self.foundations_job_function = self.patch('foundations_contrib.global_state.current_foundations_job')

        self.foundations_job = Mock()
        self.foundations_job.job_id.side_effect = ValueError()
        self.foundations_job.is_in_running_job.return_value = False
        self.foundations_job.project_name.return_value = 'some_name'

        self.foundations_job_function.return_value = self.foundations_job

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import log_manager
        log_manager.set_foundations_not_running_warning_printed(False)

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.utils')
        mock.return_when(self.mock_logger, 'foundations_events.message_router')
        return mock

    def test_whoami_user_pl(self):
        env = {"USER": "pl"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "pl")

    def test_whoami_user_kb(self):
        env = {"USER": "kb"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "kb")

    def test_whoami_uses_logname_if_user_not_set(self):
        env = {"LOGNAME": "kb"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "kb")

    def test_whoami_uses_logname_if_user_not_set_different_logname(self):
        env = {"LOGNAME": "pl"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "pl")

    def test_get_foundations_root(self):
        mock_modules = {
            "foundations": MockModule("path/to/foundations/__init__.py")
        } 

        expected_root = "path/to/foundations"

        with patch("sys.modules", mock_modules):
            self.assertEqual(utils.get_foundations_root(), expected_root)

    def test_get_foundations_root_different_root(self):
        mock_modules = {
            "foundations": MockModule("/different/for/foundations/__init__.py")
        } 

        expected_root = "/different/for/foundations"

        with patch("sys.modules", mock_modules):
            self.assertEqual(utils.get_foundations_root(), expected_root)

    def test_check_is_in_dir_root_and_file(self):
        parent_directory = "/"
        child_file = "/file"

        self.assertTrue(utils.check_is_in_dir(parent_directory, child_file))

    def test_check_is_in_dir_root_subdir_and_file(self):
        parent_directory = "/subdir"
        child_file = "/file"

        self.assertFalse(utils.check_is_in_dir(parent_directory, child_file))

    def test_check_is_in_dir_root_subdir_and_file_in_subdir(self):
        parent_directory = "/subdir"
        child_file = "/subdir/file"

        self.assertTrue(utils.check_is_in_dir(parent_directory, child_file))

    def test_check_is_in_dir_root_subdir_and_file_in_nested_subdir(self):
        parent_directory = "/subdir"
        child_file = "/subdir/nested/file"

        self.assertTrue(utils.check_is_in_dir(parent_directory, child_file))

    def test_check_is_in_dir_root_nested_subdir_and_file_not_in_nested_subdir(self):
        parent_directory = "/subdir/nested2"
        child_file = "/subdir/nested/file"

        self.assertFalse(utils.check_is_in_dir(parent_directory, child_file))

    def test_proper_subset(self):
        parent_directory = "/subdir/nested"
        child_file = "/subdir/nested"

        self.assertFalse(utils.check_is_in_dir(parent_directory, child_file))

    def test_log_warning_if_not_running_in_job_logs_correct_warning(self):
        from foundations.utils import log_warning_if_not_running_in_job

        log_warning_if_not_running_in_job(_some_function, {'result': False})
        self.mock_logger.warning.assert_called_with('Script not run with Foundations.')

    def test_log_warning_if_not_running_in_job_shows_warning_only_once_if_not_in_running_job(self):
        from foundations.utils import log_warning_if_not_running_in_job

        log_warning_if_not_running_in_job(_some_function, {'result': False})
        log_warning_if_not_running_in_job(_some_function, {'result': False})
        self.mock_logger.warning.assert_called_once_with('Script not run with Foundations.')

    def test_log_warning_if_not_running_in_job_does_not_show_warning_if_in_running_job(self):
        from foundations.utils import log_warning_if_not_running_in_job

        self.foundations_job.is_in_running_job.return_value = True
        log_warning_if_not_running_in_job(_some_function, {'result': False})
        self.mock_logger.warning.assert_not_called()

    def test_log_warning_if_not_running_in_job_runs_function_if_in_running_job(self):
        from foundations.utils import log_warning_if_not_running_in_job

        self.foundations_job.is_in_running_job.return_value = True
        some_dict = {'result': False}
        log_warning_if_not_running_in_job(_some_function, some_dict)
        self.assertTrue(some_dict['result'])

    def test_log_warning_if_not_running_in_job_does_not_run_function_if_not_in_job(self):
        from foundations.utils import log_warning_if_not_running_in_job

        self.foundations_job.is_in_running_job.return_value = False
        some_dict = {'result': False}
        log_warning_if_not_running_in_job(_some_function, some_dict)
        self.assertFalse(some_dict['result'])

def _some_function(arg):
    arg['result'] = True
