"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_ssh.ssh_job_deployment import SSHJobDeployment
from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
from foundations_ssh.ssh_listing import SSHListing
from foundations_ssh.sftp_listing import SFTPListing
from foundations_ssh.multi_ssh_bundled_pipeline_archive import MultiSSHBundledPipelineArchive
from foundations_ssh.multi_sftp_bundled_pipeline_archive import MultiSFTPBundledPipelineArchive
from foundations_ssh.ssh_file_system_bucket import SSHFileSystemBucket
from foundations_ssh.sftp_bucket import SFTPBucket


def _append_module():
    import sys
    from foundations.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])


_append_module()
