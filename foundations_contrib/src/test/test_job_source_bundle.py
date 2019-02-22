"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch, call

from foundations_contrib.job_source_bundle import JobSourceBundle
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock

class TestJobSourceBundle(Spec):

    mock_uuid4 = let_patch_mock('uuid.uuid4')
    mock_os_remove = let_patch_mock('os.remove')
    mock_os_exists = let_patch_mock('os.path.exists')
    mock_tarfile_open = let_patch_mock('tarfile.open')
    mock_change_directory = let_patch_mock('foundations_contrib.change_directory.ChangeDirectory')
    mock_mkpath = let_patch_mock('distutils.dir_util.mkpath')

    @let
    def fake_bundle_name(self):
        from faker import Faker
        return Faker().name()
    
    @let
    def fake_target_name(self):
        from faker import Faker
        return Faker().name()
    
    @let
    def fake_uuid(self):
        from faker import Faker
        return Faker().sha1()
    
    class MockFileContextManager(Mock):

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self

    class MockTarWithFiles(object):
        class MockTarInfo(object):

            def __init__(self, name):
                self.name = name

        def __enter__(self):
            return self
        
        def __iter__(self):
            return iter([self.MockTarInfo('fake_file1'), self.MockTarInfo('fake_file2')])

        def add(self, path):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self


    @patch('foundations_contrib.job_source_bundle.JobSourceBundle')
    def test_from_dict_creates_job_source_bundle(self, mock_job_source_bundle):
        job_dict = {
            'bundle_name': self.fake_bundle_name,
            'target_path': self.fake_target_name
        }
        JobSourceBundle.from_dict(job_dict)

        mock_job_source_bundle.assert_called_with(self.fake_bundle_name, self.fake_target_name)
    
    def test_from_dict_returns_job_source_bundle(self):
        job_dict = {
            'bundle_name': self.fake_bundle_name,
            'target_path': self.fake_target_name
        }
        self.assertIsInstance(JobSourceBundle.from_dict(job_dict), JobSourceBundle)
    
    @patch('foundations_contrib.job_source_bundle.JobSourceBundle')
    def test_for_deployment_creates_job_source_bundle_with_correct_arguments(self, mock_job_source_bundle):
        self.mock_uuid4.return_value = self.fake_uuid
        JobSourceBundle.for_deployment()
        mock_job_source_bundle.assert_called_with(self.fake_uuid, '../')
    
    def test_for_deployment_returns_job_source_bundle(self):
        self.assertIsInstance(JobSourceBundle.for_deployment(), JobSourceBundle)
    
    def test_job_archive_name_returns_job_archive_name(self):
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        self.assertEqual(job_source_bundle.job_archive_name(), '{}.tgz'.format(self.fake_bundle_name))
    
    def test_job_archive_returns_job_archive(self):
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        self.assertEqual(job_source_bundle.job_archive(), '{}{}.tgz'.format(self.fake_target_name, self.fake_bundle_name))
    
    def test_cleanup_checks_job_archive_exists(self):
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.cleanup()
        self.mock_os_exists.assert_called_with('{}{}.tgz'.format(self.fake_target_name, self.fake_bundle_name))
    
    def test_cleanup_calls_remove_when_job_archive_exists(self):
        self.mock_os_exists.return_value = True
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.cleanup()
        self.mock_os_remove.assert_called_with('{}{}.tgz'.format(self.fake_target_name, self.fake_bundle_name))
        
    def test_cleanup_does_not_calls_remove_when_job_archive_exists(self):
        self.mock_os_exists.return_value = False
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.cleanup()
        self.mock_os_remove.assert_not_called()
    
    def test_unbundle_calls_tarfile_open_with_correct_arguments(self):
        archive_name = '{}{}.tgz'.format(self.fake_target_name, self.fake_bundle_name)
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.unbundle('../')
        self.mock_tarfile_open.assert_called_with(archive_name, 'r:gz')
        
    def test_unbundle_calls_mkpath_with_correct_arguments(self):
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.unbundle('../')
        self.mock_mkpath.assert_called_with('../')
    
    def test_unbundle_calls_change_directory_with_correct_arguments(self):
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        self.mock_mkpath.return_value = None
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.unbundle('../')
        self.mock_change_directory.assert_called_with('../')

    def test_unbundle_extracts_from_tarfile(self):
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.unbundle('../')
        mock_tar.extractall.assert_called()

    def test_bundle_calls_tarfile_open_with_correct_arguments(self):
        archive_name = '{}{}.tgz'.format(self.fake_target_name, self.fake_bundle_name)
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.bundle()
        self.mock_tarfile_open.assert_called_with(archive_name, 'w:gz')
    
    def test_bundle_add_to_tarfile(self):
        mock_tar = self.MockFileContextManager()
        self.mock_tarfile_open.return_value = mock_tar
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.bundle()
        mock_tar.add.assert_called_with('.')
    
    @patch.object(JobSourceBundle, '_protected_file_error_messages')
    def test_bundle_iterates_through_files_and_logs(self, mock_error_message):
        mock_tar = self.MockTarWithFiles()
        self.mock_tarfile_open.return_value = mock_tar
        job_source_bundle = JobSourceBundle(self.fake_bundle_name, self.fake_target_name)
        job_source_bundle.bundle()
        file_call_1 = call('fake_file1')
        file_call_2 = call('fake_file2')
        mock_error_message.assert_has_calls([file_call_1, file_call_2])