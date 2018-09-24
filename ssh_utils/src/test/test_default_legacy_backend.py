"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

from foundations_ssh.default_legacy_backend import DefaultLegacyBackend
from foundations_ssh.remote_clock import RemoteClock
from foundations_ssh.sftp_bucket_stat_scanner import SFTPBucketStatScanner
from foundations.scheduler_legacy_backend import LegacyBackend
from foundations.global_state import config_manager

class MockLegacyBackend(object):
    def __init__(self, clock, bucket_class, code_path, archives_path, results_path):
        MockLegacyBackend.clock = clock
        MockLegacyBackend.bucket_class = bucket_class
        MockLegacyBackend.code_path = code_path
        MockLegacyBackend.archives_path = archives_path
        MockLegacyBackend.results_path = results_path

@patch("foundations.scheduler_legacy_backend.LegacyBackend", MockLegacyBackend)
class TestDefaultLegacyBackend(unittest.TestCase):
    def setUp(self):
        MockLegacyBackend.clock = None
        MockLegacyBackend.bucket_class = None
        MockLegacyBackend.code_path = None
        MockLegacyBackend.archive_path = None
        MockLegacyBackend.result_path = None

    def test_uses_legacy_backend_properly(self):
        config_manager["code_path"] = "code_path"
        config_manager["archive_path"] = "archive_path"
        config_manager["result_path"] = "result_path"

        DefaultLegacyBackend()

        self.assertTrue(isinstance(MockLegacyBackend.clock, RemoteClock))
        self.assertEqual(MockLegacyBackend.bucket_class, SFTPBucketStatScanner)
        self.assertEqual(MockLegacyBackend.code_path, "code_path")
        self.assertEqual(MockLegacyBackend.archive_path, "archive_path")
        self.assertEqual(MockLegacyBackend.result_path, "result_path")