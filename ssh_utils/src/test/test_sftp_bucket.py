"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations_ssh.sftp_bucket import SFTPBucket

class TestSFTPBucket(unittest.TestCase):
    class MockConfigManager(dict):
        def __init__(self, port=None):
            self['remote_host'] = "remote_host"
            self['remote_user'] = "remote_user"
            self['key_path'] = "key_path"

            if port:
                self['port'] = port

    class MockConnection(object):
        def __init__(self, remote_host, remote_user, private_key, port):
            self._port = port

    @patch('foundations.global_state.config_manager', MockConfigManager(22))
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_22(self):
        bucket = SFTPBucket("path")
        self.assertEqual(22, bucket._connection._port)

    @patch('foundations.global_state.config_manager', MockConfigManager(23))
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_23(self):
        bucket = SFTPBucket("path")
        self.assertEqual(23, bucket._connection._port)

    @patch('foundations.global_state.config_manager', MockConfigManager())
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_unset(self):
        bucket = SFTPBucket("path")
        self.assertEqual(22, bucket._connection._port)