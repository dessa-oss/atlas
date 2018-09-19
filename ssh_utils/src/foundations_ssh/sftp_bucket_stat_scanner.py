"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class SFTPBucketStatScanner(object):
    """This class, given a directory path, will use a configuration defined in a yaml file to return stat information for each file in the directory on a remote machine.
        Arguments:
            path: {str} -- The directory to scan on the remote machine.
    """

    def __init__(self, path):
        from paramiko.client import SSHClient

        from foundations.global_state import config_manager

        self._remote_user = config_manager['remote_user']
        self._remote_host = config_manager['remote_host']
        self._private_key_path = config_manager['key_path']
        self._port = config_manager.config().get('port', 22)
        
        self._path = path
        self._client = SSHClient()
        self._client.load_system_host_keys()

    def scan(self):
        """Returns an iterable of dicts containing file information, one for each file at the path passed into the constructor.
            The dicts have the following form:
            {
                'filename': <filename>,
                'last_modified': <metadata_modification_timestamp>,
                'owner': <user_name>
            }

        Returns:
            dict -- As described above.
        """

        import os.path as path

        with self._client as client:
            client.connect(self._remote_host, port=self._port, username=self._remote_user, key_filename=self._private_key_path)
            
            with client.open_sftp() as sftp:
                for attr in sftp.listdir_iter(path=self._path):
                    user_name = SFTPBucketScanner._translate_uid_to_user_name(client, attr.st_uid)
                    file_info = SFTPBucketScanner._construct_file_info(attr.filename, attr.st_mtime, user_name)

                    yield file_info

    @staticmethod
    def _translate_uid_to_user_name(client, uid):
        command_to_exec = "getent passwd " + str(uid) + " | cut -d: -f1"
        _, stdout_stream, _ = client.exec_command(command_to_exec)

        user_name = stdout_stream.read()
        stdout_stream.close()

        return user_name.decode("utf-8").rstrip("\n")

    @staticmethod
    def _construct_file_info(filename, last_modified, owner):
        file_info = {
            'filename': filename,
            'last_modified': last_modified,
            'owner': owner
        }

        return file_info