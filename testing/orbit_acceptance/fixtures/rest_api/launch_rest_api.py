import logging
import os

os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

from foundations_contrib.global_state import config_manager
# from foundations_rest_api.global_state import app_manager
from foundations_orbit_rest_api.global_state import app_manager
from foundations_scheduler_plugin.config.scheduler import translate
import subprocess
import yaml

import sys
redis_ip = sys.argv[1]
port = sys.argv[2]
master_ip = sys.argv[3]

submission_config = {
    'results_config': {
        'redis_end_point': redis_ip
    },
    'ssh_config': {
        'host': master_ip,
        'port': 31222,
        'code_path': '/jobs',
        'key_path': '~/.ssh/id_foundations_scheduler',
        'user': 'job-uploader'
    }
}
translated_submission_config = translate(submission_config)
configuration = config_manager.config()
configuration.update(translated_submission_config)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler('/var/foundations/orbit_test_rest_api.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# root_logger.addHandler(file_handler)

root_logger.info("Running with configuration {}".format(configuration))

app = app_manager.app()
app.run(debug=True, host='0.0.0.0', port=port)
