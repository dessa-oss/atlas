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

def _save_model_to_redis(project_name, model_name):
    from foundations_contrib.global_state import redis_connection
    import pickle

    hash_map_key = f'projects:{project_name}:model_listing'
    serialized_model_information = pickle.dumps(_get_default_model_information())
    redis_connection.hmset(hash_map_key, {model_name: serialized_model_information})


def deploy(project_name, model_name, project_directory):
    from subprocess import run
    import foundations_contrib

    _save_model_to_redis(project_name, model_name)
    
    run(['bash', './orbit/deploy_serving.sh', project_name, model_name ], cwd=foundations_contrib.root() / 'resources/model_serving/orbit')