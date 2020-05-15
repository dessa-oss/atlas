
import unittest
from mock import Mock, call, patch

from foundations_contrib.job_bundler import JobBundler
from foundations_spec import *


class TestJobBundler(Spec):

    mock_os_remove = let_patch_mock('os.remove')
    mock_tarfile_open = let_patch_mock('tarfile.open')
    mock_builtins_open = let_patch_mock('builtins.open')
    mock_yaml_dump = let_patch_mock('yaml.dump')
    mock_glob_glob = let_patch_mock('glob.glob')
    mock_os_chdir = let_patch_mock('os.chdir')
    mock_simple_temp_file_class = let_patch_mock('foundations_contrib.simple_tempfile.SimpleTempfile')
    mock_mkdtemp = let_patch_mock('tempfile.mkdtemp')

    @let
    def _default_config(self):
        return {
            'deployment_implementation': {
                'deployment_type': 'something'
            }
        }

    @let
    def redis_password(self):
        return self.faker.word()

    @let
    def temp_directory(self):
        return self.faker.uri_path()

    @set_up
    def set_up(self):
        self.mock_mkdtemp.return_value = self.temp_directory

    @staticmethod
    def _return_generator(input):
        for item in input:
            yield item

    class MockContextManager(Mock):

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self

    class MockJobSourceBundle(Mock):

        def __init__(self, archive_name):
            super().__init__()
            self._archive_name = archive_name

        def job_archive(self):
            return self._archive_name
    
        def bundle(self):
            pass
    
        def cleanup(self):
            pass

    class MockSimpleTempfile(MockContextManager):

        def __init__(self, temp_file_name):
            super().__init__()
            self.name = temp_file_name


    class MockJob(Mock):

        def serialize(self):
            pass

    def test_job_name_method_returns_job_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_name(), 'fake_name')

    def test_job_archive_name_method_returns_job_archive_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive_name(), 'fake_name.tgz')

    def test_job_archive_method_returns_job_archive(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive(), self.temp_directory + '/fake_name.tgz')

    def test_cleanup_removes_correct_files(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.cleanup()
        remove_archive = call(self.temp_directory + '/fake_name.tgz')
        remove_config = call(self.temp_directory + '/fake_name.config.yaml')
        self.mock_os_remove.assert_has_calls([remove_archive, remove_config])

    def test_unbundle_opens_correct_file(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        self.mock_tarfile_open.assert_called_with(self.temp_directory + '/fake_name.tgz', 'r:gz')

    def test_unbundle_extracts_from_tarfile(self):
        return_object = self.MockContextManager()
        self.mock_tarfile_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        return_object.extractall.assert_called()

    def test_save_config_opens_file(self):
        mock_job = self._create_mock_job()
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_builtins_open.assert_called_with(self.temp_directory + '/fake_name.config.yaml', 'w+')

    def test_save_config_dumps_to_file(self):
        mock_job = self._create_mock_job()
        return_object = self.MockContextManager()
        self.mock_builtins_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_yaml_dump.assert_called_with({'job_name': 'fake_name'}, return_object)

    def test_bundle_job_opens_file(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')

        job_bundler = JobBundler('fake_name', self._default_config, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        self.mock_tarfile_open.assert_called_with(self.temp_directory + '/fake_name.tgz', 'w:gz')

    def test_bundle_job_adds_config_files(self):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        self.mock_glob_glob.return_value = ['fake_config_filename.config.yaml']
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        add_config_call = call('fake_config_filename.config.yaml', arcname='fake_name/fake_config_filename.config.yaml')
        mock_tar.add.assert_has_calls([add_config_call])

    def _setup_archive_and_tar(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        mock_tar = self.MockContextManager()
        self.mock_tarfile_open.return_value = mock_tar

        return mock_job_source_bundle, mock_tar

    def _create_mock_job(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        return mock_job
