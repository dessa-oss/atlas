"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestBucketPipelineArchive(Spec):
    
    @let
    def bucket_klass(self):
        klass = ConditionalReturn()
        klass.return_when(self.bucket, *self.constructor_args, **self.constructor_kwargs)
        return klass

    bucket = let_mock()

    @let
    def constructor_args(self):
        return self.faker.words()
    
    @let
    def constructor_kwargs(self):
        return self.faker.pydict()

    @let
    def object_name(self):
        return self.faker.name()

    @let
    def random_data(self):
        return self.faker.uuid4()

    @let
    def random_prefix(self):
        return self.faker.uuid4()

    @let
    def file_listing_with_prefix(self):
        return [f'{self.random_prefix}/{file}' for file in self.faker.words()]

    @let
    def blob_exists(self):
        return self.faker.boolean()

    @let
    def archive(self):
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
        return BucketPipelineArchive(self.bucket_klass, *self.constructor_args, **self.constructor_kwargs)

    def test_append_binary_uploads_string_to_bucket(self):
        self.archive.append_binary(self.object_name, self.random_data, self.random_prefix)
        self.bucket.upload_from_string.assert_called_with(f'{self.random_prefix}/{self.object_name}', self.random_data)

    def test_list_files_returns_list_of_files(self):
        self.bucket.list_files = ConditionalReturn()
        self.bucket.list_files.return_when(self.file_listing_with_prefix, f'{self.random_prefix}/*')
        result = self.archive.list_files('*', self.random_prefix)
        self.assertEqual(self.file_listing_with_prefix, result)

    def test_exists_forwards_to_underlying_bucket(self):
        self.bucket.exists = ConditionalReturn()
        self.bucket.exists.return_when(self.blob_exists, f'{self.object_name}')

        self.assertEqual(self.blob_exists, self.archive.exists(self.object_name))

    def test_exists_forwards_to_underlying_bucket_with_prefix(self):
        self.bucket.exists = ConditionalReturn()
        self.bucket.exists.return_when(self.blob_exists, f'{self.random_prefix}/{self.object_name}')

        self.assertEqual(self.blob_exists, self.archive.exists(self.object_name, prefix=self.random_prefix))