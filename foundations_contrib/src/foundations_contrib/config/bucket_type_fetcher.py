"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def for_scheme(scheme, default):
    if scheme == 'sftp':
        from foundations_ssh.sftp_bucket import SFTPBucket
        return SFTPBucket
    if scheme == 'gs':
        from foundations_gcp.gcp_bucket import GCPBucket
        return GCPBucket
    if scheme == 's3':
        from foundations_aws.aws_bucket import AWSBucket
        return AWSBucket
    if scheme == 'local':
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
        return LocalFileSystemBucket
    if not scheme:
        return default

    error_message = 'Invalid uri scheme `{}` supplied - supported schemes are: sftp, gs, s3, and local'.format(scheme)
    raise ValueError(error_message)
