"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def cleanup():
    from integration.config import make_code_bucket

    bucket = make_code_bucket()
    files = list(bucket.list_files('*.tgz'))
    _log().debug('Cleaning up {}'.format(files))
    for path in files:
        _log().debug('Removing {}'.format(path))
        bucket.remove(path)

def _log():
    from foundations.global_state import log_manager
    return log_manager.get_logger(__name__)    