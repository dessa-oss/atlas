"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_ssh.sftp_bucket import SFTPBucket

class TestSFTPBucket(Spec):
    
    mock_connection_class = let_patch_mock_with_conditional_return('pysftp.Connection')
    mock_connection = let_mock()

    @set_up
    def set_up(self):
        from foundations.global_state import config_manager
        
        self.config_manager = config_manager
        self.config_manager["remote_host"] = "remote_host"
        self.config_manager["remote_user"] = "remote_user"
        self.config_manager["key_path"] = "key_path"

        mock_cd_object = Mock()
        mock_cd_object.__enter__ = lambda *args: None
        mock_cd_object.__exit__ = lambda *args: None

        self.mock_connection.cd.return_value = mock_cd_object

    @tear_down
    def tear_down(self):
        self.config_manager.config().pop("port", None)

    def _set_up_connection(self, port=22):
        self.mock_connection_class.return_when(self.mock_connection, self.config_manager['remote_host'], self.config_manager['remote_user'], private_key=self.config_manager['key_path'], port=port)

    def test_upload_from_string_supports_strings(self):
        self._set_up_connection()
        bucket = SFTPBucket('path')
        bucket.upload_from_string('/path/to/some/file', 'some string')

    def test_set_port_24(self):
        self._set_up_connection(port=24)
        self.config_manager["port"] = 24
        SFTPBucket("path")

    def test_set_port_23(self):
        self._set_up_connection(port=23)
        self.config_manager["port"] = 23
        SFTPBucket("path")

    def test_set_port_unset(self):
        self._set_up_connection()
        SFTPBucket("path")