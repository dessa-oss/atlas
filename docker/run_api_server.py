import logging
import os

from foundations import config_manager
from foundations_rest_api.global_state import app_manager

config_manager.config()["redis_url"] = os.environ["REDIS_URL"]

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('/var/foundations/rest_api.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

root_logger.info(str(config_manager.config()))

app = app_manager.app()
app.run(host="0.0.0.0", port=37722)
