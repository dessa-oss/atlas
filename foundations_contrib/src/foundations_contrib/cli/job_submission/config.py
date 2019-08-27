"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def load(config_name):
    import sys
    from foundations_contrib.cli.typed_config_listing import TypedConfigListing
    from foundations_scheduler_plugin.config.scheduler import translate

    listing = TypedConfigListing('submission')
    
    if listing.config_path(config_name) is None:
        print(f"Could not find submission configuration with name: `{config_name}`")
        sys.exit(1)
    else:
        listing.update_config_manager_with_config(config_name, translate)