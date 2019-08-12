"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_spec import *

from foundations.artifacts.syncable_directory import SyncableDirectory

from integration.config import ARCHIVE_ROOT

from pathlib import Path

class TestUploadModelPackageWithSyncableDirectory(Spec):
    
    key = 'model'
    package_name = 'model_package'


    @let
    def model_id(self):
        return self.faker.uuid4()

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        import shutil

        if Path('tmp/').exists():
            shutil.rmtree('tmp/')

    @let
    def model_result_path(self):
        return Path(ARCHIVE_ROOT) / self.model_id / (self.package_name + '_directories') / self.key

    @let
    def model_name_based_result_path(self):
        archive_end_point_from_config = '/tmp/foundations_test'
        return Path('{}/archive'.format(archive_end_point_from_config)) / self.model_name / (self.package_name + '_directories') / self.key

    def test_upload_model_package_with_sycable_directory(self):
        model_package_path = 'integration/fixtures/model_package'

        syncable_directory = SyncableDirectory(self.key, model_package_path, self.model_id, None, auto_download=False, package_name=self.package_name)
        syncable_directory.upload()

        with open(self.model_result_path / 'some_content.txt', 'r') as file:
            self.assertEqual('Content of file.', file.read())

    def test_upload_model_package_with_syncable_directory_from_config(self):
        from foundations_contrib.global_state import config_manager

        config_manager.reset()
        config_manager.add_simple_config_path('integration/fixtures/config/archive.config.yaml')

        project_directory_from_config = config_manager['result_path']
        self.assertEqual('integration/fixtures/model_package', project_directory_from_config)

        syncable_directory = SyncableDirectory(self.key, project_directory_from_config, self.model_name, None, auto_download=False, package_name=self.package_name)
        syncable_directory.upload()

        with open(self.model_name_based_result_path / 'some_content.txt', 'r') as file:
            self.assertEqual('Content of file.', file.read())