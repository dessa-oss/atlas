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
    result = _artifact_path_and_end_point_implementation(config)

    result.update({
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
        'remote_user': config['ssh_config'].get('user', 'foundations'),
        'code_path': config['ssh_config']['code_path'],
        'port': config['ssh_config'].get('port', 22),
        'result_path': config['ssh_config']['result_path'],
        'key_path': config['ssh_config']['key_path'],
        'remote_host': config['ssh_config']['host'],
        'run_script_environment': {
            'log_level': _log_level(config)
        }
    })
    return result

def _log_level(config):
    return config.get('log_level', 'INFO')

def _cache_implementation(config):
    from foundations_contrib.config.mixin import cache_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    cache_end_point = config['cache_config']['end_point']
    return cache_implementation(cache_end_point, LocalFileSystemBucket)

def _redis_url(config):
    return config['results_config'].get('redis_end_point', 'redis://localhost:6379')

def _project_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import project_listing_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    project_path = join(result_end_point, 'projects')
    return project_listing_implementation(result_end_point, DeploymentSSHBucket)

def _deployment_implementation():
    from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
    return {
        'deployment_type': SFTPJobDeployment
    }

def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_listing_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    return archive_listing_implementation(result_end_point, DeploymentSSHBucket.bucket_from_single_path)

def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

    return archive_implementation(result_end_point, DeploymentSSHBucket.bucket_from_single_path)

def _obfuscate_foundations(config):
    return config.get('obfuscate_foundations', False)

def _artifact_path(config):
    results_config = config['results_config']
    artifact_path = results_config.get('artifact_path')
    return artifact_path or 'results'

def _artifact_path_and_end_point_implementation(config):
    from foundations_contrib.config.mixin import results_artifact_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    artifact_config = {'artifact_path': _artifact_path(config)}
    artifact_end_point_config = config['results_config'].get('artifact_end_point') or ''
    artifact_config['artifact_end_point'] = artifact_end_point_config
    return {
        'artifact_path': artifact_config['artifact_path'],
        'artifact_end_point_implementation': results_artifact_implementation(artifact_config, LocalFileSystemBucket)
    }
