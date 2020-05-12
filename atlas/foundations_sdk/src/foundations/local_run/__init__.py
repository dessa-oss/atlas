
_exception_happened = False
import yaml


def set_up_default_environment_if_present():
    import redis
    from foundations_contrib.global_state import redis_connection

    if not _in_command_line():
        if load_execution_environment():
            # This needs to be refactored to throw an exception at the message router level
            try:
                redis_connection.ping()
                set_up_job_environment()
            except redis.exceptions.ConnectionError:
                _get_logger().warn(
                    "Foundations has been imported, but a connection to Redis could not be established. "
                    "No foundations code will run and a job will not be generated. "
                    "Please make sure the server components started up correctly."
                )

        else:
            _get_logger().warn(
                "Foundations has been imported, but no default configuration file has been found. "
                "Refer to the documentation for more information. "
                "Without a default configuration file, no foundations code will be executed."
            )


def load_execution_environment():
    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_internal.config.execution import translate

    listing = TypedConfigListing("execution")
    if listing.config_path("default"):
        listing.update_config_manager_with_config("default", translate)
        return True

    return False


def set_up_job_environment():
    from foundations_events.producers.jobs import QueueJob
    from foundations_events.producers.jobs import RunJob
    from foundations_contrib.global_state import (
        current_foundations_context,
        message_router,
        config_manager,
    )
    import atexit

    config_manager["_is_deployment"] = True
    _get_logger().debug(
        f"Foundations has been run with the following configuration:\n"
        f"{yaml.dump(config_manager.config(), default_flow_style=False)}"
    )
    pipeline_context = current_foundations_context().pipeline_context()
    _set_job_state(pipeline_context)

    QueueJob(message_router, current_foundations_context()).push_message()
    RunJob(message_router, current_foundations_context()).push_message()

    atexit.register(_at_exit_callback)
    _set_up_exception_handling()


def _set_up_exception_handling():
    import sys

    global _exception_happened
    _exception_happened = False
    sys.excepthook = _handle_exception


def _get_logger():
    from foundations_contrib.global_state import log_manager

    return log_manager.get_logger(__name__)


def _in_command_line():
    import os

    return os.environ.get("FOUNDATIONS_COMMAND_LINE", "False") == "True"


def _handle_exception(exception_type, value, traceback):
    import sys

    global _exception_happened
    _exception_happened = True
    sys.__excepthook__(exception_type, value, traceback)


def _at_exit_callback():
    from foundations_contrib.global_state import (
        current_foundations_context,
        message_router,
    )
    from foundations_contrib.archiving.upload_artifacts import upload_artifacts
    from foundations_events.producers.jobs import CompleteJob
    from foundations_events.producers.jobs import FailedJob

    global _exception_happened

    upload_artifacts(current_foundations_context().job_id())
    # This try-except block should be refactored at a later date

    if _exception_happened:
        FailedJob(
            message_router,
            current_foundations_context(),
            {"type": Exception, "exception": "", "traceback": []},
        ).push_message()
    else:
        CompleteJob(message_router, current_foundations_context()).push_message()


def _set_job_state(pipeline_context):
    from uuid import uuid4
    import os

    pipeline_context.file_name = os.environ.get("FOUNDATIONS_JOB_ID", str(uuid4()))
    pipeline_context.provenance.project_name = os.environ.get(
        "FOUNDATIONS_PROJECT_NAME",
        os.environ.get("PROJECT_NAME", _default_project_name()),
    )


def _default_project_name():
    import os.path

    return os.path.basename(os.getcwd())


def _default_environment_present():
    from os.path import basename

    environments = _environment_listing()
    environments = [basename(path) for path in environments]
    return "default.config.yaml" in environments


def _environment_listing():
    from foundations_core_cli.environment_fetcher import EnvironmentFetcher

    environment_fetcher = EnvironmentFetcher()
    local_environments, global_environments = environment_fetcher.get_all_environments()
    local_environments = local_environments or []
    global_environments = global_environments or []

    return local_environments + global_environments
