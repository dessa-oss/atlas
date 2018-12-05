"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

from foundations_ssh.default_legacy_backend import default_legacy_backend
from foundations_ssh.sftp_bucket_stat_scanner import SFTPBucketStatScanner
from foundations.global_state import config_manager

class MockClock(object):
    def __init__(self):
        pass

class MockLegacyBackend(object):
    def __init__(self, clock, bucket_class, code_path, archive_path, result_path):
        self.clock = clock
        self.bucket_class = bucket_class
        self.code_path = code_path
        self.archive_path = archive_path
        self.result_path = result_path

@patch("foundations_contrib.scheduler_legacy_backend.LegacyBackend", MockLegacyBackend)
@patch("foundations_ssh.remote_clock.RemoteClock", MockClock)
class TestDefaultLegacyBackend(unittest.TestCase):
    def test_uses_legacy_backend_properly(self):
        config_manager["code_path"] = "code_path"
        config_manager["archive_path"] = "archive_path"
        config_manager["result_path"] = "result_path"

        backend = default_legacy_backend()

        self.assertTrue(isinstance(backend.clock, MockClock))
        self.assertEqual(backend.bucket_class, SFTPBucketStatScanner)
        self.assertEqual(backend.code_path, "code_path")
        self.assertEqual(backend.archive_path, "archive_path")
        self.assertEqual(backend.result_path, "result_path")

    def test_uses_legacy_backend_properly_different_config(self):
        config_manager["code_path"] = "code_path2"
        config_manager["archive_path"] = "archive_path2"
        config_manager["result_path"] = "result_path2"

        backend = default_legacy_backend()

        self.assertTrue(isinstance(backend.clock, MockClock))
        self.assertEqual(backend.bucket_class, SFTPBucketStatScanner)
        self.assertEqual(backend.code_path, "code_path2")
        self.assertEqual(backend.archive_path, "archive_path2")
        self.assertEqual(backend.result_path, "result_path2")