"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def archive_implementation(result_end_point, default_bucket_type):
    from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
    from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive

    bucket_type, uri = _parse_bucket_type_and_uri(result_end_point, default_bucket_type)

    return {
        'archive_type': BucketPipelineArchive,
        'constructor_arguments': [bucket_type, uri.netloc + uri.path]
    }
    
def _parse_bucket_type_and_uri(result_end_point, default_bucket_type):
    from os.path import join
    from urllib.parse import urlparse

    from foundations_contrib.config.bucket_type_fetcher import for_scheme

    archive_path = join(result_end_point, 'archive')
    uri = urlparse(archive_path)
    scheme = uri.scheme
    if scheme == '':
        scheme = None
    bucket_type = for_scheme(scheme, default_bucket_type)
    return bucket_type, uri

