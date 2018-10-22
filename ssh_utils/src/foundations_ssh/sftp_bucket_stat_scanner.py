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
        from foundations_ssh.paramiko_manager import ParamikoManager

        self._path = path
        self._paramiko = ParamikoManager()

        self._health_check()

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

        with self._paramiko as client:
            with client.get_paramiko_sftp() as sftp:
                for attr in sftp.listdir_iter(path=self._path):
                    user_name = self._translate_uid_to_user_name(attr.st_uid)
                    file_info = SFTPBucketStatScanner._construct_file_info(attr.filename, attr.st_mtime, user_name)

                    yield file_info

    def _translate_uid_to_user_name(self, uid):
        # assumes client is connected
        command_to_exec = "id -un " + str(uid)
        return self._paramiko.exec_command(command_to_exec)

    def _health_check(self):
        with self._paramiko as client:
            with client.get_paramiko_sftp() as sftp:
                try:
                    sftp.lstat(self._path)
                except IOError:
                    raise IOError("SFTPBucketStatScanner could not connect to path " + self._path)

    @staticmethod
    def _construct_file_info(filename, last_modified, owner):
        file_info = {
            'filename': filename,
            'last_modified': last_modified,
            'owner': owner
        }

        return file_info