"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_ssh.ssh_listing import SSHListing
from foundations_ssh.sftp_listing import SFTPListing
from foundations_ssh.sftp_bucket import SFTPBucket
from foundations_ssh.versioning import __version__


def _append_module():
    import sys
    from foundations_internal import global_state
    
    global_state.module_manager.append_module(sys.modules[__name__])


_append_module()

