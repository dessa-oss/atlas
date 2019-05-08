"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.data_loader import DataLoader
from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

class TestDataLoader(Spec):

    local_file_system_bucket_class = let_patch_mock('foundations_contrib.local_file_system_bucket.LocalFileSystemBucket', ConditionalReturn())
    local_file_system_bucket_instance = let_mock()

    @let
    def file_name_with_scheme(self):
        import os.path as path
        return 'local://' + path.join(self.file_path, self.file_name)

    @let
    def file_path(self):
        return self.faker.file_path()

    @let
    def file_name(self):
        return self.faker.file_name()

    @let
    def fake_data(self):
        return self.faker.sentence()

    @let
    def fake_serialized_data(self):
        from foundations_internal.serializer import serialize
        return serialize(self.fake_data)

    def test_data_loader_uses_local_file_system_bucket_for_local_path(self):
        self.local_file_system_bucket_class.return_when(self.local_file_system_bucket_instance, self.file_path)
        self.local_file_system_bucket_instance.download_as_string = ConditionalReturn()
        self.local_file_system_bucket_instance.download_as_string.return_when(self.fake_serialized_data, self.file_name)

        data_loader = DataLoader()
        data = data_loader.load_data(self.file_name_with_scheme)
        self.assertEqual(self.fake_data, data)