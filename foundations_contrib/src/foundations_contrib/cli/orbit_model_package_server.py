"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import foundations
import subprocess
import pickle
from foundations.utils import _log


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

def _retrieve_configuration_secrets():
    import yaml
    import base64
    import os
    from os.path import expanduser, join

    _log().debug('Attmepting to download configuration from kubernetes')
    process = subprocess.run(['bash', '-c', 'kubectl -n foundations-scheduler-test get secret job-server-private-keys -o yaml'], stdout=subprocess.PIPE)
    secret_data = yaml.load(process.stdout)
    base64.b64decode(secret_data['data']['job-uploader'])
    expected_key_path = join(expanduser('~'), '.ssh/id_foundations_scheduler')
    if os.path.exists(expected_key_path):
        _log().debug('Removing the old configuration from')
        os.remove(expected_key_path)

    with open(expected_key_path, 'w+b') as ssh_file:
        ssh_file.write(base64.b64decode(secret_data['data']['job-uploader']))
        ssh_file.close()
        _log().debug('Successfully saved keys from kubernetes')

    os.chmod(expected_key_path, 400)
    _log().debug('Settings for kubernetes configured successfully')

def _save_model_to_redis(project_name, model_name):
    from foundations_contrib.global_state import redis_connection
    project_hash_map_key = f'projects:{project_name}:model_listing'
    serialized_model_information = pickle.dumps(_get_default_model_information())
    redis_connection.hmset(project_hash_map_key, {model_name: serialized_model_information})


def _model_exists_in_project(project_name, model_name):
    from foundations_contrib.global_state import redis_connection
    project_hash_map_key = f'projects:{project_name}:model_listing'
    retrieved_results = redis_connection.hgetall(project_hash_map_key)
    decoded_results = {key.decode(): value for key, value in retrieved_results.items()}

    if model_name in decoded_results:
        return True
    return False


def _upload_model_directory(project_name, model_name, project_directory):
    from foundations.artifacts.syncable_directory import SyncableDirectory
    local_directory_key = '{}-{}'.format(project_name, model_name)

    syncable_directory = SyncableDirectory(
        local_directory_key,
        project_directory,
        local_directory_key,
        None,
        auto_download=False)
    syncable_directory.upload()


def _launch_model_package(project_name, model_name):
    import foundations_contrib

    return subprocess.run(
        ['bash', './deploy_serving.sh', project_name, model_name ], 
        cwd=foundations_contrib.root() / 'resources/model_serving/orbit'
    )


def _setup_environment(project_name, env):
    foundations.set_project_name(project_name)
    foundations.set_environment(env)
    _retrieve_configuration_secrets()


def deploy(project_name, model_name, project_directory, env='local'):
    try:
        _setup_environment(project_name, env)
        print('************* Deploy Executed ***************')
        if _model_exists_in_project(project_name, model_name):
            return False

        _save_model_to_redis(project_name, model_name)
        print('************* Saved to Redis ***************')
        _upload_model_directory(project_name, model_name, project_directory)
        print('************* Uploaded to Directory ***************')
        _launch_model_package(project_name, model_name)
        print('************* Launched Model Package ***************')
        return True
    except:
        return False
