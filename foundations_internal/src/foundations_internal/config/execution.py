

def translate(config):
    from jsonschema import validate
    import foundations_contrib
    import yaml

    with open(
        f"{foundations_contrib.root()}/resources/config_validation/execution.yaml"
    ) as file:
        schema = yaml.load(file.read())
    validate(instance=config, schema=schema)

    result_end_point = config["results_config"].get(
        "archive_end_point", _get_default_archive_end_point()
    )

    result = {
        "artifact_archive_implementation": _archive_implementation(result_end_point),
        "job_source_archive_implementation": _archive_implementation(result_end_point),
        "miscellaneous_archive_implementation": _archive_implementation(
            result_end_point
        ),
        "persisted_data_archive_implementation": _archive_implementation(
            result_end_point
        ),
        "provenance_archive_implementation": _archive_implementation(result_end_point),
        "stage_log_archive_implementation": _archive_implementation(result_end_point),
        "archive_listing_implementation": _archive_listing_implementation(
            result_end_point
        ),
        "project_listing_implementation": _project_listing_implementation(
            result_end_point
        ),
        "redis_url": _redis_url(config),
        "log_level": _log_level(config),
        "run_script_environment": {
            "log_level": _log_level(config),
        },
        "artifact_path": ".",
        "archive_end_point": result_end_point,
    }
    return result


def _get_default_archive_end_point():
    from foundations_contrib.utils import foundations_home
    from os.path import expanduser
    from os.path import join

    return join(expanduser(foundations_home()), "job_data")


def _log_level(config):
    return config.get("log_level", "INFO")


def _redis_url(config):
    return config["results_config"].get("redis_end_point", "redis://localhost:6379")


def _project_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import project_listing_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return project_listing_implementation(result_end_point, LocalFileSystemBucket)


def _deployment_implementation():
    from foundations_local_docker_scheduler_plugin.job_deployment import JobDeployment

    return {"deployment_type": JobDeployment}


def _archive_listing_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_listing_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return archive_listing_implementation(result_end_point, LocalFileSystemBucket)


def _archive_implementation(result_end_point):
    from foundations_contrib.config.mixin import archive_implementation
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    return archive_implementation(result_end_point, LocalFileSystemBucket)
