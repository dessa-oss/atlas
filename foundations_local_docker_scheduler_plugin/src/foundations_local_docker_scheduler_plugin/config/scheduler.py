from os.path import join

def translate(config):
    result = {
        'deployment_implementation': _deployment_implementation(),
        'redis_url': config.get('redis_url', 'redis://localhost:6379'),
        'worker_container_overrides': config.get('worker', {}),
        # 'job_store_root': config['job_store_root'],
        'job_results_root': config['job_results_root'],
        'working_dir_root': config['working_dir_root'],
        'scheduler_url': config['scheduler_url'],
        'container_config_root': config['container_config_root']
    }

    return result

def _deployment_implementation():
    from foundations_local_docker_scheduler_plugin.job_deployment import JobDeployment
    return {
        'deployment_type': JobDeployment
    }
