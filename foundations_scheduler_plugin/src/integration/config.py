from foundations_spec.extensions import get_network_address

def _load_config():
    import os
    from foundations_contrib.global_state import config_manager
    from foundations_scheduler_plugin.config.scheduler import translate
    from foundations_contrib.cli.typed_config_listing import TypedConfigListing

    translated_config = translate({'results_config': {}, 'ssh_config': {}})
    config_manager.config().update(translated_config)

    if 'FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL' in os.environ:
        redis_url = os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL']
        config_manager['result_url'] = redis_url

_load_config()