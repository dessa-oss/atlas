

def cleanup():
    from acceptance.config import make_code_bucket

    bucket = make_code_bucket()
    files = list(bucket.list_files('*.tgz'))
    _log().debug('Cleaning up {}'.format(files))
    for path in files:
        _log().debug('Removing {}'.format(path))
        bucket.remove(path)


def _log():
    from foundations.global_state import log_manager
    return log_manager.get_logger(__name__)
