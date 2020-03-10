import sys
from foundations_contrib.global_state import config_manager
from foundations_rest_api.global_state import app_manager
from foundations_local_docker_scheduler_plugin.job_deployment import JobDeployment
import logging
import os
import os.path as path


def config_logging(foundations_home):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    if not path.exists(f"{foundations_home}/logs"):
        print(foundations_home)
        os.mkdir(f"{foundations_home}/logs")
    file_handler = logging.FileHandler(f"{foundations_home}/logs/atlas_rest_api.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def set_submission_config(redis_url, foundations_scheduler_url):
    translated_submission_config = {
        "redis_url": redis_url,
        "deployment_implementation": {"deployment_type": JobDeployment,},
        "scheduler_url": foundations_scheduler_url,
    }

    config_manager.config().update(translated_submission_config)


if __name__ == "__main__":
    import os

    FOUNDATIONS_HOME = os.path.abspath(os.path.expanduser(".foundations"))
    PORT = sys.argv[1]

    config_logging(FOUNDATIONS_HOME)
    set_submission_config(
        os.getenv("REDIS_URL"), os.getenv("FOUNDATIONS_SCHEDULER_URL")
    )
    print(f'Running Atlas API with Redis at: {config_manager.config()["redis_url"]}')
    app = app_manager.app()
    app.run(host="127.0.0.1", port=PORT, debug=True)
