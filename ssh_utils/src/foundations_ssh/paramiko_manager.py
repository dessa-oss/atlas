"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 06 2018
"""

class ParamikoManager(object):
    """A convenience wrapper that loads configuration for ssh commands executed via paramiko.
    """

    def __init__(self):
        from paramiko import SSHClient
        
        from foundations.global_state import config_manager

        self._remote_user = config_manager['remote_user']
        self._remote_host = config_manager['remote_host']
        self._private_key_path = config_manager['key_path']
        self._port = config_manager.config().get('port', 22)
        
        self._client = SSHClient()
        self._client.load_system_host_keys()
        self._is_connected = False

    def __enter__(self):
        """Connect to the remote host as defined in the config manager.

        Returns:
            self -- This object, once connected.
        """

        self._client.connect(self._remote_host, port=self._port, username=self._remote_user, key_filename=self._private_key_path)
        self._is_connected = True
        return self

    def __exit__(self, *args):
        """Disconnect from the remote host.
            Arguments:
                *args: {args_set} -- Ignored
        """

        self._client.close()
        self._is_connected = False

    def get_paramiko_sftp(self):
        """If connected, return an SFTP client from the underlying client.  Return None otherwise.

        Returns:
            sftp_client -- SFTPClient from Paramiko.
        """

        if not self._is_connected:
            return None
        
        return self._client.open_sftp()
    
    def exec_command(self, command_string):
        """No longer supported way to execute commands on a remote system
        
        Arguments:
            command_string {str} -- The command to execute
        
        Raises:
            Exception -- An exception indicating that this is an invalid operator
        """

        raise Exception('Unsupported operation')