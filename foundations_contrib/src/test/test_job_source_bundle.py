"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_contrib.job_source_bundle import JobSourceBundle
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock

class TestJobSourceBundle(Spec):

    mock_uuid4 = let_patch_mock('uuid.uuid4')
    mock_os_remove = let_patch_mock('os.remove')
    mock_os_exists = let_patch_mock('os.path.exists')
    
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
        





    


