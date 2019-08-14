"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import foundations
import subprocess

def _get_default_model_information():
    return {
        'status': 'activated',
        'default': False,
        'created_by': '',
        'created_at': '',
        'description': '',
        'entrypoints': {},
        'validation_metrics': {}
    }

def _save_model_to_redis(project_name, model_name):
    from foundations_contrib.global_state import redis_connection
    import pickle

    hash_map_key = f'projects:{project_name}:model_listing'
    serialized_model_information = pickle.dumps(_get_default_model_information())
    redis_connection.hmset(hash_map_key, {model_name: serialized_model_information})

def _upload_model_directory(project_name, model_name, project_directory):
    from foundations.artifacts.syncable_directory import SyncableDirectory
    local_directory_key = '{}-{}'.format(project_name, model_name)

    syncable_directory = SyncableDirectory(local_directory_key, project_directory, local_directory_key, None)
    syncable_directory.upload()

def _launch_model_package(project_name, model_name):
    import foundations_contrib

    return subprocess.run(
        ['bash', './deploy_serving.sh', project_name, model_name ], 
        cwd=foundations_contrib.root() / 'resources/model_serving/orbit'
    )

def _setup_environment(project_name, model_name, env):
    from foundations_contrib.global_state import current_foundations_context
    from foundations_internal.pipeline_context_wrapper import PipelineContextWrapper

    foundations.set_project_name(project_name)
    foundations.set_environment(env)
    # pipeline_context_wrapper = PipelineContextWrapper(current_foundations_context().pipeline_context())


def deploy(project_name, model_name, project_directory, env='local'):
    _setup_environment(project_name, model_name, env)

    _save_model_to_redis(project_name, model_name)

    _upload_model_directory(project_name, model_name, project_directory)

    _launch_model_package(project_name, model_name)    