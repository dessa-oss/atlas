
def load(config_name):
    import sys
    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_local_docker_scheduler_plugin.config.scheduler import translate

    listing = TypedConfigListing('submission')
    
    if listing.config_path(config_name) is None:
        print(f"Could not find submission configuration with name: `{config_name}`")
        sys.exit(1)
    else:
        listing.update_config_manager_with_config(config_name, translate)