"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, call, patch

from foundations_contrib.job_bundler import JobBundler
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock


class TestJobBundler(Spec):

    mock_os_remove = let_patch_mock('os.remove')
    mock_tarfile_open = let_patch_mock('tarfile.open')
    mock_builtins_open = let_patch_mock('builtins.open')
    mock_yaml_dump = let_patch_mock('yaml.dump')
    mock_glob_glob = let_patch_mock('glob.glob')
    mock_global_state = let_patch_mock('foundations.global_state')
    mock_os_chdir = let_patch_mock('os.chdir')

    class MockFileContextManager(Mock):

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

    class MockSimpleTempfile(object):

        def __init__(self, temp_file_name=''):
            #super().__init__()
            self._temp_file_name = temp_file_name

        @property
        def name(self):
            return self._temp_file_name

    def test_job_name_method_returns_job_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_name(), 'fake_name')

    def test_job_archive_name_method_returns_job_archive_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive_name(), 'fake_name.tgz')

    def test_job_archive_method_returns_job_archive(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive(), '../fake_name.tgz')

    def test_cleanup_removes_correct_files(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.cleanup()
        remove_archive = call('../fake_name.tgz')
        remove_bin = call('fake_name.bin')
        remove_config = call('fake_name.config.yaml')
        self.mock_os_remove.assert_has_calls([remove_archive, remove_bin, remove_config])

    def test_unbundle_opens_correct_file(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        self.mock_tarfile_open.assert_called_with('../fake_name.tgz', 'r:gz')

    def test_unbundle_extracts_from_tarfile(self):
        return_object = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        return_object.extractall.assert_called()

    def test_save_job_opens_file(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_job()
        self.mock_builtins_open.assert_called_with('fake_name.bin', 'w+b')

    def test_save_job_writes_to_file(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        return_object = self.MockFileContextManager()
        self.mock_builtins_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_job()
        return_object.write.assert_called_with('something')

    def test_save_config_opens_file(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_builtins_open.assert_called_with('fake_name.config.yaml', 'w+')

    def test_save_config_dumps_to_file(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        return_object = self.MockFileContextManager()
        self.mock_builtins_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_yaml_dump.assert_called_with({'job_name': 'fake_name'}, return_object)

    def test_bundle_job_opens_file(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        self.mock_tarfile_open.assert_called_with('../fake_name.tgz', 'w:gz')

    def test_bundle_job_adds_archive_and_binary_to_tarball(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        add_archive_call = call('fake_source_archive_name', arcname='fake_name/job.tgz')
        add_binary_call = call('fake_name.bin', arcname='fake_name/fake_name.bin')
        mock_tar.add.assert_has_calls([add_archive_call, add_binary_call], any_order=True)

    def test_bundle_job_adds_config_files(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        self.mock_glob_glob.return_value = ['fake_config_filename.config.yaml']
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        add_config_call = call('fake_config_filename.config.yaml', arcname='fake_name/fake_config_filename.config.yaml')
        mock_tar.add.assert_has_calls([add_config_call])

    def test_bundle_job_adds_modules(self):
        import foundations_internal

        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar

        with patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names',
                          return_value=[('fake_module_name', 'fake_module_directory')]):
            job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
            job_bundler._bundle_job()

        self.mock_os_chdir.assert_has_calls([call('fake_module_directory')])
        mock_tar.add.assert_has_calls([call('.', arcname='fake_name/fake_module_name')])
