"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from uuid import uuid4

# separates test runs
TEST_UUID = str(uuid4())


def _code_bucket():
    return 'foundations-code-test'


def make_code_bucket():
    from foundations import PrefixedBucket
    from foundations_aws import AWSBucket

    return PrefixedBucket(TEST_UUID, AWSBucket, _code_bucket())


def _result_bucket():
    return 'foundations-results-test'


def make_result_bucket():
    from foundations import PrefixedBucket
    from foundations_aws import AWSBucket

    return PrefixedBucket(TEST_UUID, AWSBucket, _result_bucket())


def _config():
    from foundations import config_manager
    from foundations import PrefixedBucket, BucketPipelineArchive, BucketPipelineListing
    from foundations_aws import AWSBucket

    # archive implementations
    archive_implementation = {
        'archive_type': BucketPipelineArchive,
        'constructor_arguments': [PrefixedBucket, TEST_UUID, AWSBucket, _result_bucket()],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': BucketPipelineListing,
        'constructor_arguments': [PrefixedBucket, TEST_UUID, AWSBucket, _result_bucket()],
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation
    config_manager['run_script_environment'] = {'enable_stages': True}

    # quiet logs
    config_manager['log_level'] = 'ERROR'


_config()
