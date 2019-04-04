from foundations_spec.extensions import get_network_address

def _load_config():
    import os
    from foundations_contrib.global_state import config_manager
    
    config_manager['remote_host'] = 'localhost'
    config_manager['remote_user'] = 'job-uploader'
    config_manager['port'] = 31222
    config_manager['key_path'] = os.path.expanduser('~/.ssh/id_foundations_scheduler')
    config_manager['code_path'] = '/jobs'
    config_manager['redis_url'] = 'redis://{}:6379'.format(get_network_address('docker0'))

_load_config()