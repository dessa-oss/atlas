
from pathlib import Path


def safely_create_directory(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)


def dump_dict_to_yaml_file(data, filepath):
    import yaml
    import os
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filepath, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def dump_all_config_files():
    import yaml

    # ======== Configuration Start
    from pathlib import Path

    HOME = Path.home()
    config_directories = [] 

    # === Default paths
    FOUNDATIONS_HOME = HOME / '.foundations'
    config_directories.append(FOUNDATIONS_HOME)
    
    WORKING_DIRECTORY = FOUNDATIONS_HOME / 'local_docker_scheduler' / 'work_dir'
    config_directories.append(WORKING_DIRECTORY)
    
    JOB_RESULTS = FOUNDATIONS_HOME / 'job_data'
    config_directories.append(JOB_RESULTS)
    
    PERSISTENT_STORAGE = FOUNDATIONS_HOME / 'database'
    config_directories.append(PERSISTENT_STORAGE)
    
    DOCKER_SOCKET = "/var/run/docker.sock"
    DOCKER_CONFIG = HOME / '.docker'
    config_directories.append(DOCKER_CONFIG)
    
    CONTAINER_CONFIG_ROOT = FOUNDATIONS_HOME / 'config' / 'local_docker_scheduler' / 'worker_config'
    config_directories.append(CONTAINER_CONFIG_ROOT)
    
    TENSORBOARD_WORK_DIR = FOUNDATIONS_HOME / 'tensorboard' / 'work_dir'
    config_directories.append(TENSORBOARD_WORK_DIR)

    LOCAL_CONFIG_ROOT = FOUNDATIONS_HOME / 'config'
    config_directories.append(LOCAL_CONFIG_ROOT)

    # === Default configuration paths
    
    SCHEDULER_SUBMISSION_CONFIG_PATH = CONTAINER_CONFIG_ROOT / 'submission' / 'scheduler.config.yaml'
    config_directories.append(CONTAINER_CONFIG_ROOT / 'submission')
    
    SCHEDULER_EXECUTION_CONFIG_PATH = CONTAINER_CONFIG_ROOT / 'execution' / 'default.config.yaml'
    config_directories.append(CONTAINER_CONFIG_ROOT / 'execution')
    
    LOCAL_SUBMISSION_CONFIG_PATH = LOCAL_CONFIG_ROOT / 'submission' / 'scheduler.config.yaml'
    config_directories.append(CONTAINER_CONFIG_ROOT / 'submission')
    
    LOCAL_EXECUTION_CONFIG_PATH = LOCAL_CONFIG_ROOT / 'execution' / 'default.config.yaml'
    config_directories.append(CONTAINER_CONFIG_ROOT / 'execution')
    
    TRACKER_CLIENT_PLUGINS_PATH = LOCAL_CONFIG_ROOT / 'local_docker_scheduler' / 'tracker_client_plugins.yaml'
    config_directories.append(CONTAINER_CONFIG_ROOT / 'local_docker_scheduler')
    
    DATABASE_CONFIG_PATH = LOCAL_CONFIG_ROOT / 'local_docker_scheduler' / 'database.config.yaml'
    SERVICE_CONFIG_PATH = LOCAL_CONFIG_ROOT / 'service.config.yaml'
    
    # ======== make mount points
    for directory in config_directories:
        safely_create_directory(directory)

    # === Default ports
    SCHEDULER_PORT = 5000
    REDIS_PORT = 5556

    # === Default Docker information
    with open("manifest.yaml", 'r') as f:
        images = yaml.load(f, Loader=yaml.FullLoader)

    REDIS_IMAGE_NAME = images['tracker']['name']
    REDIS_IMAGE_TAG = images['tracker']['tag']
    REDIS_CONTAINER_NAME = "tracker"

    SCHEDULER_IMAGE_NAME = images['scheduler']['name']
    SCHEDULER_IMAGE_TAG = images['scheduler']['tag']
    SCHEDULER_CONTAINER_NAME = "scheduler"

    # === Standard Configuration dictionaries

    LOCAL_SUBMISSION_CONFIG = {
        "job_deployment_env": "local_docker_scheduler_plugin",
        "job_results_root": str(JOB_RESULTS),
        "working_dir_root": str(WORKING_DIRECTORY),
        "scheduler_url": "http://127.0.0.1:{}".format(SCHEDULER_PORT),
        "container_config_root": str(CONTAINER_CONFIG_ROOT),
        "cache_config": {
            "end_point": "/cache_end_point"
        }
    }

    LOCAL_EXECUTION_CONFIG = {
        "results_config": {
            "redis_end_point": "redis://127.0.0.1:{}".format(REDIS_PORT),
            "archive_end_point": str(JOB_RESULTS)
        },
        "cache_config": {
            "end_point": "/cache"
        },
        "log_level": "INFO"
    }

    TRACKER_CLIENT_PLUGINS = {
        "redis_tracker_client": {
            "host": REDIS_CONTAINER_NAME,
            "port": 6379
        }
    }

    DATABASE_CONFIG = {
        "failed_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "failed_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "running_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "running_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "completed_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "completed_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "queue": {
            "type": "redis_connection.RedisList",
            "args": {
                "key": "queued_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        }
    }

    SERVICE_CONFIG = {
        "persistent_storage": str(PERSISTENT_STORAGE),
        "docker_socket": DOCKER_SOCKET,
        "docker_config": str(DOCKER_CONFIG),
        "tensorboard_work_dir": str(TENSORBOARD_WORK_DIR),
        "docker": {
            "redis": {
                "image": "{}:{}".format(REDIS_IMAGE_NAME, REDIS_IMAGE_TAG),
                "container": REDIS_CONTAINER_NAME
            },
            "scheduler": {
                "image": "{}:{}".format(SCHEDULER_IMAGE_NAME, SCHEDULER_IMAGE_TAG),
                "container": SCHEDULER_CONTAINER_NAME
            }
        }
    }

    # === OS-Specific Configuration dictionaries

    SCHEDULER_SUBMISSION_CONFIG = {
        "job_deployment_env": "local_docker_scheduler_plugin",
        "job_results_root": str(JOB_RESULTS),
        "working_dir_root": str(WORKING_DIRECTORY),
        "scheduler_url": "http://{}:{}".format(SCHEDULER_CONTAINER_NAME, SCHEDULER_PORT),
        "container_config_root": str(CONTAINER_CONFIG_ROOT),
        "cache_config": {
            "end_point": "/cache_end_point"
        }
    }

    SCHEDULER_EXECUTION_CONFIG = {
        "results_config": {
            "redis_end_point": "redis://{}:6379".format(REDIS_CONTAINER_NAME),
            "archive_end_point": str(JOB_RESULTS),
        },
        "cache_config": {
            "end_point": "/cache"
        },
        "log_level": "INFO"
    }

    # ======== Configuration End
    dump_dict_to_yaml_file(LOCAL_SUBMISSION_CONFIG, LOCAL_SUBMISSION_CONFIG_PATH)
    dump_dict_to_yaml_file(LOCAL_EXECUTION_CONFIG, LOCAL_EXECUTION_CONFIG_PATH)
    dump_dict_to_yaml_file(SCHEDULER_SUBMISSION_CONFIG, SCHEDULER_SUBMISSION_CONFIG_PATH)
    dump_dict_to_yaml_file(SCHEDULER_EXECUTION_CONFIG, SCHEDULER_EXECUTION_CONFIG_PATH)
    dump_dict_to_yaml_file(TRACKER_CLIENT_PLUGINS, TRACKER_CLIENT_PLUGINS_PATH)
    dump_dict_to_yaml_file(DATABASE_CONFIG, DATABASE_CONFIG_PATH)
    dump_dict_to_yaml_file(SERVICE_CONFIG, SERVICE_CONFIG_PATH)


if __name__ == "__main__":
    dump_all_config_files()
