"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from os.path import join
from foundations_internal.config.common_translate import get_translate_implementation


def get_translator_config(config_option):
    config_options = {
        'get_result_end_point': _get_result_end_point,
        'archive_implementation': _archive_implementation,
        'archive_listing_implementation': _archive_listing_implementation,
        'deployment_implementation': _deployment_implementation,
        'project_listing_implementation': _project_listing_implementation,
        'cache_implementation': _cache_implementation,
    }
    return config_options[config_option]

def _get_result_end_point(config):
    return config['results_config'].get('archive_end_point', _get_default_archive_end_point())

def _get_default_archive_end_point():
    from os.path import expanduser
    from os.path import join

    return join(expanduser('~'), '.foundations/job_data')

def _cache_implementation(config):
    from foundations_contrib.config.mixin import cache_implementation
    from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    cache_config = config['cache_config']
    if 'end_point' in cache_config:
        cache_end_point = cache_config['end_point']
        return cache_implementation(cache_end_point, LocalFileSystemBucket)

    cache_end_point = _get_default_archive_end_point()
    cache_path = join(cache_end_point, 'cache')
    return {
        'cache_type': LocalFileSystemCacheBackend,
        'constructor_arguments': [cache_path]
    }

def _project_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import project_listing_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return project_listing_implementation(result_end_point, LocalFileSystemBucket)

def _deployment_implementation():
    from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
    return {
        'deployment_type': LocalShellJobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_listing_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return archive_listing_implementation(result_end_point, LocalFileSystemBucket)

def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return archive_implementation(result_end_point, LocalFileSystemBucket)

translate = get_translate_implementation(get_translator_config)
