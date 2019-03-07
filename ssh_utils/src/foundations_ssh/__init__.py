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
from foundations_ssh.sftp_bucket import SFTPBucket
from foundations_ssh.versioning import __version__

import foundations_ssh.config


def _append_module():
    import sys
    from foundations_internal import global_state
    
    global_state.module_manager.append_module(sys.modules[__name__])


_append_module()


def _inject_config_translate():
    from foundations_internal.global_state import config_translator
    import foundations_ssh.config.ssh_config_translate as translator

    config_translator.add_translator('ssh', translator)


_inject_config_translate()
