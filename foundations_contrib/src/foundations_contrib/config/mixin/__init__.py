"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def archive_implementation(result_end_point, default_bucket_type):
    from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
    return _storage_implementation('archive_type', BucketPipelineArchive, 'archive', result_end_point, default_bucket_type)
    
def archive_listing_implementation(result_end_point, default_bucket_type):
    from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing
    return _storage_implementation('archive_listing_type', BucketPipelineListing, 'archive', result_end_point, default_bucket_type)
    
def project_listing_implementation(result_end_point, default_bucket_type):
    from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing
    return _storage_implementation('project_listing_type', BucketPipelineListing, 'projects', result_end_point, default_bucket_type)
    
def cache_implementation(cache_end_point, default_bucket_type):
    from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
    from foundations_contrib.bucket_cache_backend_for_config import BucketCacheBackendForConfig

    return _storage_implementation('cache_type', BucketCacheBackendForConfig, 'cache', cache_end_point, default_bucket_type)

def _storage_implementation(type_key, type_value, type_name, result_end_point, default_bucket_type):
    bucket_type, uri = _parse_bucket_type_and_uri(type_name, result_end_point, default_bucket_type)

    return {
        type_key: type_value,
        'constructor_arguments': [bucket_type, uri.netloc + uri.path]
    }

def _parse_bucket_type_and_uri(type_name, result_end_point, default_bucket_type):
    from os.path import join
    from urllib.parse import urlparse

    from foundations_contrib.config.bucket_type_fetcher import for_scheme

    archive_path = join(result_end_point, type_name)
    uri = urlparse(archive_path)
    scheme = uri.scheme
    if scheme == '':
        scheme = None
    bucket_type = for_scheme(scheme, default_bucket_type)
    return bucket_type, uri