

def for_scheme(scheme, default):
    callback_mapping = {
        'local': _get_local_bucket,
        None: lambda: default
    }
    bucket_callback = callback_mapping.get(scheme, _invalid_scheme_callback(scheme))
    return bucket_callback()

def _invalid_scheme_callback(scheme):
    def _raise_error():
        error_message = 'Invalid uri scheme `{}` supplied - supported schemes are: local'.format(scheme)
        raise ValueError(error_message)
    return _raise_error

def _get_local_bucket():
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
    return LocalFileSystemBucket

