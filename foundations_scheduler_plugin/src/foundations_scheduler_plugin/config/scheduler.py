from os.path import join

def translate(config):
    from foundations_contrib.helpers.shell import find_bash
    from foundations_contrib.config.mixin import ssh_configuration

    result = {
        'deployment_implementation': _deployment_implementation(),
        'redis_url': _redis_url(config),
        'shell_command': find_bash(),
        'obfuscate_foundations': _obfuscate_foundations(config),
        'worker_container_overrides': config.get('worker', {})
    }
    result.update(ssh_configuration(config))

    return result 

def _redis_url(config):
    return config['results_config'].get('redis_end_point', 'redis://localhost:6379')

def _deployment_implementation():
    from foundations_scheduler_plugin.job_deployment import JobDeployment
    return {
        'deployment_type': JobDeployment
    }

def _obfuscate_foundations(config):
    return config.get('obfuscate_foundations', False)