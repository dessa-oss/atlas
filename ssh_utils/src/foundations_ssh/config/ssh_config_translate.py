"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from os.path import join

def translate(config):
    from foundations_contrib.helpers.shell import find_bash

    result_end_point = config['results_config']['archive_end_point']

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
        'obfuscate': _obfuscate(config),
    }

def _log_level(config):
    return config.get('log_level', 'INFO')

def _cache_implementation(config):
    from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend

    cache_end_point = config['cache_config']['end_point']
    cache_path = join(cache_end_point, 'cache')
    return {
        'cache_type': LocalFileSystemCacheBackend,
        'constructor_arguments': [cache_path]
    }

def _redis_url(config):
    return config['results_config'].get('redis_end_point', 'redis://localhost:6379')

def _project_listing_implementation(result_end_point):
    from foundations.bucket_pipeline_listing import BucketPipelineListing
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    project_path = join(result_end_point, 'projects')
    return {
        'project_listing_type': BucketPipelineListing,
        'constructor_arguments': [DeploymentSSHBucket, project_path, project_path]
    }

def _deployment_implementation():
    from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
    return {
        'deployment_type': SFTPJobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations.bucket_pipeline_listing import BucketPipelineListing
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    archive_path = join(result_end_point, 'archive')
    return {
        'archive_listing_type': BucketPipelineListing,
        'constructor_arguments': [DeploymentSSHBucket, archive_path, archive_path]
    }

def _archive_implementation(result_end_point):
    from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    archive_path = join(result_end_point, 'archive')
    return {
        'archive_type': BucketPipelineArchive,
        'constructor_arguments': [DeploymentSSHBucket, archive_path, archive_path]
    }

def _obfuscate(config):
    return config.get('obfuscate', False)

