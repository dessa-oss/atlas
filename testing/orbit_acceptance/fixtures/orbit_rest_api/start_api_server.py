# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018

from foundations_orbit_rest_api.global_state import app_manager
import logging
import os

os.environ['FOUNDATIONS_SCHEDULER_URL'] = 'http://' + os.environ['LOCAL_DOCKER_SCHEDULER_HOST'] + ':5000'
orbit_rest_api_port = os.environ.get('REST_API_PORT', 37222)

app = app_manager.app()

# disable flask default logs and send logs to files
from flask.logging import default_handler
app.logger.removeHandler(default_handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_path = f'{os.environ.get("FOUNDATIONS_HOME")}/logs/orbit_rest_api.log'
handler = logging.FileHandler(log_path)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

# run the application
app.run(debug=True, host='127.0.0.1', port=orbit_rest_api_port)
