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
        @classmethod
        def __init__(cls, remote_host, remote_user, private_key, port):
            cls.port = port

    def setUp(self):
        self.MockConnection.port = None

    @patch('foundations.global_state.config_manager', MockConfigManager(22))
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_22(self):
        SFTPBucket("path")
        self.assertEqual(22, self.MockConnection.port)

    @patch('foundations.global_state.config_manager', MockConfigManager(23))
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_23(self):
        SFTPBucket("path")
        self.assertEqual(23, self.MockConnection.port)

    @patch('foundations.global_state.config_manager', MockConfigManager())
    @patch('pysftp.Connection', MockConnection)
    def test_set_port_unset(self):
        SFTPBucket("path")
        self.assertEqual(22, self.MockConnection.port)