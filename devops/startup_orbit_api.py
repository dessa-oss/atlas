# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Susan Davis <s.davis@dessa.com>, 12 2019

try:
    from foundations_contrib.global_state import config_manager
    from foundations_orbit_rest_api.global_state import app_manager
    import logging
    import os
    import sys

    foundations_home = os.path.abspath(os.path.expanduser(os.environ.get('FOUNDATIONS_HOME', '~/.foundations')))
    redis_url = f"redis://{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', 6379)}"

    config_manager.config()['redis_url'] = redis_url

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(f'{foundations_home}/logs/orbit_rest_api.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    print(f'Running Orbit API with Redis at: {config_manager.config()["redis_url"]}')

    app = app_manager.app()
    app.run(host='127.0.0.1', port=sys.argv[1], debug=True)

except Exception as e:
    print(e)
    sys.exit(1)