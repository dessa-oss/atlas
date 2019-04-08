"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def for_scheme(scheme, default):
    callback_mapping = { 
        'sftp': _get_sftp_bucket, 
        'gs': _get_gcp_bucket, 
        's3': _get_aws_bucket, 
        'local': _get_local_bucket, 
        None: lambda: default
    }
    bucket_callback = callback_mapping.get(scheme, _invalid_scheme_callback(scheme))
    return bucket_callback()

def _invalid_scheme_callback(scheme):
    def _raise_error():
        error_message = 'Invalid uri scheme `{}` supplied - supported schemes are: sftp, gs, s3, and local'.format(scheme)
        raise ValueError(error_message)
    return _raise_error

def _get_local_bucket():
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
    return LocalFileSystemBucket

def _get_aws_bucket():
    from foundations_aws.aws_bucket import AWSBucket
    return AWSBucket

def _get_gcp_bucket():
    from foundations_gcp.gcp_bucket import GCPBucket
    return GCPBucket

def _get_sftp_bucket():
    from foundations_ssh.sftp_bucket import SFTPBucket
    return SFTPBucket
