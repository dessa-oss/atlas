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
        'artifact_path_and_end_point_implementation': _artifact_path_and_end_point_implementation,
        'archive_implementation': _archive_implementation,
        'archive_listing_implementation': _archive_listing_implementation,
        'deployment_implementation': _deployment_implementation,
        'project_listing_implementation': _project_listing_implementation,
        'cache_implementation': _cache_implementation,
    }
    return config_options[config_option]

def _get_result_end_point(config):
    return config['results_config']['archive_end_point']

def _cache_implementation(config):
    from foundations_contrib.config.mixin import cache_implementation
    from foundations_gcp.gcp_bucket import GCPBucket

    cache_end_point = config['cache_config']['end_point']
    return cache_implementation(cache_end_point, GCPBucket)

def _project_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import project_listing_implementation
    from foundations_gcp.gcp_bucket import GCPBucket

    return project_listing_implementation(result_end_point, GCPBucket)

def _deployment_implementation():
    from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
    return {
        'deployment_type': SFTPJobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_listing_implementation
    from foundations_gcp.gcp_bucket import GCPBucket

    return archive_listing_implementation(result_end_point, GCPBucket)

def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_gcp.gcp_bucket import GCPBucket

    return archive_implementation(result_end_point, GCPBucket)

def _artifact_path(config):
    results_config = config['results_config']
    artifact_path = results_config.get('artifact_path')
    return artifact_path or 'results'

def _artifact_path_and_end_point_implementation(config):
    from foundations_contrib.config.mixin import results_artifact_implementation
    from foundations_gcp.gcp_bucket import GCPBucket

    artifact_config = {'artifact_path': _artifact_path(config)}
    artifact_end_point_config = config['results_config'].get('artifact_end_point') or ''
    artifact_config['artifact_end_point'] = artifact_end_point_config
    return {
        'artifact_path': artifact_config['artifact_path'],
        'artifact_end_point_implementation': results_artifact_implementation(artifact_config, GCPBucket)
    }

translate = get_translate_implementation(get_translator_config)
