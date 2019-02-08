"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_contrib.deployment_context_bucket import DeploymentContextBucket


class DeploymentSSHBucket(DeploymentContextBucket):

    def __init__(self, sftp_path, file_system_path):
        from foundations_contrib.lazy_bucket import LazyBucket
        from foundations_ssh.sftp_bucket import SFTPBucket
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        sftp_bucket = LazyBucket(lambda: SFTPBucket(sftp_path))
        local_bucket = LazyBucket(lambda: LocalFileSystemBucket(file_system_path))
        super(DeploymentSSHBucket, self).__init__(sftp_bucket, local_bucket)
