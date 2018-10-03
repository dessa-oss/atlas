"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

from foundations_ssh.remote_clock import RemoteClock

class MockParamikoManager(object):
    def __init__(self):
        self._is_connected = False

    def __enter__(self):
        self._is_connected = True
        return self

    def __exit__(self, *args):
        self._is_connected = False

    def exec_command(self, command):
        if not self._is_connected:
            return None

        return MockParamikoManager.timestamp_string

class TestRemoteClock(unittest.TestCase):
    def setUp(self):
        MockParamikoManager.timestamp_string = None

    def _set_clock_string(self, stamp_string):
        MockParamikoManager.timestamp_string = stamp_string

    @patch("foundations_ssh.paramiko_manager.ParamikoManager", MockParamikoManager)
    def test_time(self):
        self._set_clock_string("12345")
        self.assertEqual(RemoteClock().time(), 12345)

    @patch("foundations_ssh.paramiko_manager.ParamikoManager", MockParamikoManager)
    def test_different_time(self):
        self._set_clock_string("41414")
        self.assertEqual(RemoteClock().time(), 41414)