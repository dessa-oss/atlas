"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
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
    import subprocess
    import stat
    import base64
    import os
    from os.path import expanduser, join

    process = subprocess.run(['bash', '-c', 'kubectl -n foundations-scheduler-test get secret job-server-private-keys -o yaml'], stdout=subprocess.PIPE)
    secret_data = yaml.load(process.stdout)
    base64.b64decode(secret_data['data']['job-uploader'])
    expected_key_path = join(expanduser('~'), '.ssh/id_foundations_scheduler')
    
    if os.path.exists(expected_key_path):
        os.remove(expected_key_path)

    with open(expected_key_path, 'w+b') as ssh_file:
        ssh_file.write(base64.b64decode(secret_data['data']['job-uploader']))

    os.chmod(expected_key_path, stat.S_IREAD)

def _save_model_to_redis(project_name, model_name, model_details):
    import pickle
    from foundations_contrib.global_state import redis_connection
    project_model_listings = _retrieve_project_from_redis(project_name)
    serialized_model_information = pickle.dumps(model_details)
    
    project_model_listings.update({model_name: serialized_model_information})
    redis_connection.hmset(f'projects:{project_name}:model_listing', project_model_listings)

def _save_project_to_redis(project_name):
    from time import time
    from foundations_contrib.global_state import redis_connection
    
    timestamp = time()
    redis_connection.execute_command('ZADD', 'projects', 'NX', timestamp, project_name)


def _retrieve_project_from_redis(project_name):
    from foundations_contrib.global_state import redis_connection
    return redis_connection.hgetall(f'projects:{project_name}:model_listing')

def _retrieve_model_details_from_redis(project_name, model_name):
    import pickle
    from foundations_contrib.global_state import redis_connection

    project_model_listings = _retrieve_project_from_redis(project_name)
    deserialised = {key.decode(): value for key, value in project_model_listings.items()}
    model_details = deserialised.get(model_name, None)
    if model_details:
        return pickle.loads(model_details)
    return {}

def _update_model_in_redis(project_name, model_name, dict_of_updates = {}):
    import pickle
    from foundations_contrib.global_state import redis_connection
    model_details = _retrieve_model_details_from_redis(project_name, model_name)

    for key, value in dict_of_updates.items():
        model_details[key] = value
    serialized_model_information = pickle.dumps(model_details) 
    
    project_model_listings = _retrieve_project_from_redis(project_name)
    if model_name in project_model_listings:
        project_model_listings.pop(model_name)

    project_model_listings.update({model_name: serialized_model_information})
    redis_connection.hmset(f'projects:{project_name}:model_listing', project_model_listings)

def _is_model_activated(project_name, model_name):
    details = _retrieve_model_details_from_redis(project_name, model_name)
    return details['status'] == 'activated'

def _model_exists_in_project(project_name, model_name):
    project_model_listings = _retrieve_project_from_redis(project_name)
    decoded_results = {key.decode(): value for key, value in project_model_listings.items()}

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
        package_name='artifacts')
        
    syncable_directory.upload()

def _orbit_command_handler(project_name, model_name, file_name):
    import foundations_contrib
    import subprocess

    process_result = subprocess.run(
        ['bash', 
        file_name, 
        project_name,
        model_name, 'none' ], 
        cwd=foundations_contrib.root() / 'resources/model_serving/orbit'
    )
    return process_result.returncode == 0

def _launch_model_package(project_name, model_name):
    return _orbit_command_handler(project_name, model_name, './deploy_serving.sh')

def _remove_model_package(project_name, model_name):
    return _orbit_command_handler(project_name, model_name, './remove_deployment.sh')

def _setup_environment(project_name, env):
    import foundations
    foundations.set_project_name(project_name)
    foundations.set_environment(env)
    _retrieve_configuration_secrets()

def deploy(project_name, model_name, project_directory, env='local'):
    _setup_environment(project_name, env)

    if _model_exists_in_project(project_name, model_name):
        if _is_model_activated(project_name, model_name):
            return False
    
    _save_project_to_redis(project_name)

    _save_model_to_redis(project_name, model_name, _get_default_model_information())
    _upload_model_directory(project_name, model_name, project_directory)
    return _launch_model_package(project_name, model_name)

def stop(project_name, model_name, env='local'):
    _setup_environment(project_name, env)
    _update_model_in_redis(project_name, model_name, {'status': 'deactivated'})
    return _remove_model_package(project_name, model_name)

def _remove_project_model_from_redis(project_name, model_name):
    from foundations_contrib.global_state import redis_connection
    project_hash_map_key = f'projects:{project_name}:model_listing'
    redis_connection.hdel(project_hash_map_key, model_name)

def destroy(project_name, model_name, env='local'):
    _setup_environment(project_name, env)
    _remove_project_model_from_redis(project_name, model_name)
    return _remove_model_package(project_name, model_name)