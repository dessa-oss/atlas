"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def create_config_file():
    import yaml
    import os
    from foundations_core_cli.typed_config_listing import TypedConfigListing

    os.makedirs('config/execution', exist_ok=True)

    if TypedConfigListing('execution').config_path('default') is None:
        with open('config/execution/default.config.yaml', 'w+') as file:
            config = {'results_config': {}, 'cache_config': {}}
            serialized_config = yaml.dump(config)
            file.write(serialized_config)