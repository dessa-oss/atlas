import os

from foundations_rest_api.global_state import app_manager
from foundations.global_state import deployment_manager, config_manager

config_manager.config()["redis_url"] = os.environ["REDIS_URL"]

for key, value in config_manager.config().items():
    print(key, value)

app = app_manager.app()
app.run(host="0.0.0.0", port=37722)
