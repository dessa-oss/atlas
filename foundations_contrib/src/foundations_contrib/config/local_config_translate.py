"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from os.path import join

def translate(config):
    from foundations_contrib.helpers.shell import find_bash

    result_end_point = config['results_config'].get('archive_end_point', _get_default_archive_end_point())

    return {
        'artifact_archive_implementation': _archive_implementation(result_end_point),
        'job_source_archive_implementation': _archive_implementation(result_end_point),
        'miscellaneous_archive_implementation': _archive_implementation(result_end_point),
        'persisted_data_archive_implementation': _archive_implementation(result_end_point),
        'provenance_archive_implementation': _archive_implementation(result_end_point),
        'stage_log_archive_implementation': _archive_implementation(result_end_point),
        'archive_listing_implementation': _archive_listing_implementation(result_end_point),
        'deployment_implementation': _deployment_implementation(),
        'project_listing_implementation': _project_listing_implementation(result_end_point),
        'redis_url': _redis_url(config),
        'cache_implementation': _cache_implementation(config),
        'log_level': _log_level(config),
        'shell_command': find_bash(),
        'obfuscate_foundations': _obfuscate_foundations(config),
        'run_script_environment': {
            'log_level': _log_level(config)
        }
        
    }

def _get_default_archive_end_point():
    from os.path import expanduser
    from os.path import join

    return join(expanduser('~'), '.foundations/job_data')

def _log_level(config):
    return config.get('log_level', 'INFO')

def _cache_implementation(config):
    from foundations_contrib.config.mixin import storage_implementation
    from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend
    from foundations_contrib.bucket_cache_backend import BucketCacheBackend
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    cache_config = config['cache_config']
    if 'end_point' in cache_config:
        cache_end_point = cache_config['end_point']
        return storage_implementation('cache_type', BucketCacheBackend, cache_end_point, LocalFileSystemBucket)
    
    cache_end_point = _get_default_archive_end_point()
    cache_path = join(cache_end_point, 'cache')
    return {
        'cache_type': LocalFileSystemCacheBackend,
        'constructor_arguments': [cache_path]
    }

def _redis_url(config):
    return config['results_config'].get('redis_end_point', 'redis://localhost:6379')

def _project_listing_implementation(result_end_point):
    from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing

    project_path = join(result_end_point, 'projects')
    return {
        'project_listing_type': LocalFileSystemPipelineListing,
        'constructor_arguments': [project_path]
    }

def _deployment_implementation():
    from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
    return {
        'deployment_type': LocalShellJobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import storage_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
    from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

    return storage_implementation('archive_listing_type', BucketPipelineListing, result_end_point, LocalFileSystemBucket)

def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return archive_implementation(result_end_point, LocalFileSystemBucket)

def _obfuscate_foundations(config):
    return config.get('obfuscate_foundations', False)