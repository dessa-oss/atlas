def _get_docker_adapter():
    import ifaddr

    for adapter in ifaddr.get_adapters():
        if adapter.name == 'docker0':
            return adapter

def _redis_ip():
    docker_adapter = _get_docker_adapter()
    
    for ip in docker_adapter.ips:
        if isinstance(ip.ip, str):
            return ip.ip


def _load_config():
    import os
    from foundations_contrib.global_state import config_manager
    
    config_manager['remote_host'] = 'localhost'
    config_manager['remote_user'] = 'job-uploader'
    config_manager['port'] = 31222
    config_manager['key_path'] = os.path.expanduser('~/.ssh/id_foundations_scheduler')
    config_manager['code_path'] = '/jobs'
    config_manager['redis_url'] = 'redis://{}:6379'.format(_redis_ip())

_load_config()