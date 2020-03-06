

from os import getcwd, environ

# separates test runs
from uuid import uuid4

if "TEST_UUID" not in environ:
    environ["TEST_UUID"] = str(uuid4())
    environ["ARCHIVE_ROOT"] = getcwd() + "/tmp/archives_{}/archive".format(
        environ["TEST_UUID"]
    )

TEST_UUID = environ["TEST_UUID"]
ARCHIVE_ROOT = environ["ARCHIVE_ROOT"]


def _config():
    from foundations_contrib.global_state import config_manager
    from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
    from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing

    config_manager["job_notification_channel"] = "spamity"
    config_manager["job_notification_channel_id"] = "CM6U16G4D"

    # below is used to create archives for all different types

    archive_implementation = {
        "archive_type": LocalFileSystemPipelineArchive,
        "constructor_arguments": [ARCHIVE_ROOT],
    }
    config_manager["archive_listing_implementation"] = {
        "archive_listing_type": LocalFileSystemPipelineListing,
        "constructor_arguments": [ARCHIVE_ROOT],
    }
    config_manager["persisted_data_archive_implementation"] = archive_implementation
    config_manager["provenance_archive_implementation"] = archive_implementation
    config_manager["job_source_archive_implementation"] = archive_implementation
    config_manager["artifact_archive_implementation"] = archive_implementation
    config_manager["miscellaneous_archive_implementation"] = archive_implementation
    config_manager["artifact_path"] = "results"
    config_manager["log_level"] = "CRITICAL"


_config()
