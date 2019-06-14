from foundations_spec.extensions import get_network_address

def _load_config():
    import os
    from foundations_contrib.global_state import config_manager
    
    running_on_ci = os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE'

    if running_on_ci:
        scheduler_host = os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST']
        redis_url = os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL']
    else:
        scheduler_host = 'localhost'
        redis_url = 'redis://{}:6379'.format(get_network_address('docker0'))

    config_manager['remote_host'] = scheduler_host
    config_manager['remote_user'] = 'job-uploader'
    config_manager['port'] = 31222
    config_manager['code_path'] = '/jobs'
    config_manager['redis_url'] = redis_url
    config_manager['artifact_path'] = 'results'

_load_config()