"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations.scheduler_legacy_backend import LegacyBackend

class DefaultLegacyBackend(LegacyBackend):
    """This is the same as the LegacyBackend, but it initializes itself using predefined configs from a yaml file.
    """

    def __init__(self):
        from foundations_ssh.remote_clock import RemoteClock
        from foundations_ssh.sftp_bucket_stat_scanner import SFTPBucketStatScanner

        from foundations.global_state import config_manager

        clock = RemoteClock()

        code_path = config_manager['code_path']
        archive_path = config_manager['archive_path']
        result_path = config_manager['result_path']

        super(DefaultLegacyBackend, self).__init__(clock, SFTPBucketStatScanner, code_path, archive_path, result_path)