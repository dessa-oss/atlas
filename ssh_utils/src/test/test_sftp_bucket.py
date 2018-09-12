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
    class MockConnection(object):
        @classmethod
        def __init__(cls, remote_host, remote_user, private_key, port):
            cls.port = port

    def setUp(self):
        from foundations.global_state import config_manager
        
        self.config_manager = config_manager
        self.config_manager["remote_host"] = "remote_host"
        self.config_manager["remote_user"] = "remote_user"
        self.config_manager["key_path"] = "key_path"

    def tearDown(self):
        self.MockConnection.port = None
        self.config_manager.config().pop("port", None)

    @patch('pysftp.Connection', MockConnection)
    def test_set_port_24(self):
        self.config_manager["port"] = 24
        SFTPBucket("path")
        self.assertEqual(24, self.MockConnection.port)

    @patch('pysftp.Connection', MockConnection)
    def test_set_port_23(self):
        self.config_manager["port"] = 23
        SFTPBucket("path")
        self.assertEqual(23, self.MockConnection.port)

    @patch('pysftp.Connection', MockConnection)
    def test_set_port_unset(self):
        SFTPBucket("path")
        self.assertEqual(22, self.MockConnection.port)