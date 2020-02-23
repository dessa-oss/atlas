

def get_translate_implementation(get_translator_config):

    get_result_end_point = get_translator_config("get_result_end_point")
    archive_implementation = get_translator_config("archive_implementation")
    archive_listing_implementation = get_translator_config(
        "archive_listing_implementation"
    )
    deployment_implementation = get_translator_config("deployment_implementation")
    project_listing_implementation = get_translator_config(
        "project_listing_implementation"
    )

    def _translate(config):
        from foundations_contrib.helpers.shell import find_bash

        result_end_point = get_result_end_point(config)

        result = {
            "artifact_archive_implementation": archive_implementation(result_end_point),
            "job_source_archive_implementation": archive_implementation(
                result_end_point
            ),
            "miscellaneous_archive_implementation": archive_implementation(
                result_end_point
            ),
            "persisted_data_archive_implementation": archive_implementation(
                result_end_point
            ),
            "provenance_archive_implementation": archive_implementation(
                result_end_point
            ),
            "archive_listing_implementation": archive_listing_implementation(
                result_end_point
            ),
            "deployment_implementation": deployment_implementation(),
            "project_listing_implementation": project_listing_implementation(
                result_end_point
            ),
            "redis_url": _redis_url(config),
            "artifact_path": _artifact_path(config),
            "log_level": _log_level(config),
            "shell_command": find_bash(),
            "run_script_environment": {"log_level": _log_level(config),},
        }
        if "worker" in config:
            worker_config = get_translator_config("worker")
            result.update(worker_config(config))
        return result

    return _translate


def _log_level(config):
    return config.get("log_level", "INFO")


def _redis_url(config):
    return config["results_config"].get("redis_end_point", "redis://localhost:6379")


def _artifact_path(config):
    return config["results_config"].get("artifact_path", "results")
