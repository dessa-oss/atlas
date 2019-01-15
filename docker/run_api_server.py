import logging
import os

from foundations import config_manager
from foundations_rest_api.global_state import app_manager

configuration = config_manager.config()
configuration["redis_url"] = os.environ["REDIS_URL"]

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('/var/foundations/rest_api.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

root_logger.info("Running with configuration {}".format(configuration))

app = app_manager.app()

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "request-originating server addresses"
    return response