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
        'worker': _worker_container_overrides
    }
    return config_options[config_option]


def _get_result_end_point(config):
    return config['results_config']['archive_end_point']

def _cache_implementation(config):
    from foundations_contrib.config.mixin import cache_implementation
    from foundations_contrib.bucket_cache_backend_for_config import BucketCacheBackendForConfig
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    cache_end_point = config['cache_config']['end_point']
    return cache_implementation(cache_end_point, LocalFileSystemBucket)

def _project_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import project_listing_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    return project_listing_implementation(result_end_point, DeploymentSSHBucket.bucket_from_single_path)

def _deployment_implementation():
    from foundations_scheduler_plugin.job_deployment import JobDeployment
    return {
        'deployment_type': JobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_listing_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    return archive_listing_implementation(result_end_point, DeploymentSSHBucket.bucket_from_single_path)

def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    return archive_implementation(result_end_point, DeploymentSSHBucket.bucket_from_single_path)

def _worker_container_overrides(config):
    return {
        'worker_container_overrides': config['worker']
    }

translate = get_translate_implementation(get_translator_config)
