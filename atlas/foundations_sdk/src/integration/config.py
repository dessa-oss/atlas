

def _config():
    from uuid import uuid4
    from os import getcwd
    from foundations_contrib.global_state import (
        config_manager,
        current_foundations_context,
    )
    from foundations_contrib.global_state import config_manager
    from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
    from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing

    # ensure a job uuid is set
    current_foundations_context().job_id = "integration-test-job"

    # separates test runs
    test_uuid = uuid4()

    # below is used to create archives for all different types
    archive_root = getcwd() + "/tmp/archives_{}".format(test_uuid)

    archive_implementation = {
        "archive_type": LocalFileSystemPipelineArchive,
        "constructor_arguments": [archive_root],
    }
    config_manager["archive_listing_implementation"] = {
        "archive_listing_type": LocalFileSystemPipelineListing,
        "constructor_arguments": [archive_root],
    }
    config_manager["persisted_data_archive_implementation"] = archive_implementation
    config_manager["provenance_archive_implementation"] = archive_implementation
    config_manager["job_source_archive_implementation"] = archive_implementation
    config_manager["artifact_archive_implementation"] = archive_implementation
    config_manager["miscellaneous_archive_implementation"] = archive_implementation


_config()
