from vcat.simple_tempfile import SimpleTempfile


class SSHFileSystemBucket(object):

    def __init__(self, shell_command, user, host, ssh_key_path, path):
        from vcat_ssh.ssh_utils import SSHUtils

        self._path = path
        self._config = {
            "shell_command": shell_command,
            "remote_user": user,
            "remote_host": host,
            "key_path": ssh_key_path,
        }
        self._ssh_utils = SSHUtils(self._config)

    def upload_from_string(self, name, data):
        with SimpleTempfile('w+b') as temp_file:
            temp_file.write_and_flush(data)
            self._ssh_utils.execute_to_remote_scp(temp_file.name, self._remote_path(name))

    def upload_from_file(self, name, input_file):
        self._ssh_utils.execute_to_remote_scp(input_file.name, self._remote_path(name))

    def exists(self, name):
        from subprocess import call

        command = self._list_files_command(name)
        return call(command) == 0

    def download_as_string(self, name):
        with SimpleTempfile('w+b') as temp_file:
            self._ssh_utils.execute_to_local_scp(self._remote_path(name), temp_file.name)
            return temp_file.read()

    def download_to_file(self, name, output_file):
        self._ssh_utils.execute_to_local_scp(self._remote_path(name), output_file.name)

    def list_files(self, pathname):
        from os.path import basename

        file_paths = self._list_remote_files(pathname)
        return [basename(path) for path in file_paths]

    def _remote_path(self, name):
        return self._path + '/' + name

    def _list_remote_files(self, pathname):
        from subprocess import Popen
        from subprocess import PIPE

        command = self._list_files_command(pathname)
        process = Popen(command, stdout=PIPE)
        listing, _ = process.communicate()
        listing = listing.strip()
        return listing.split("\n")

    def _list_files_command(self, pathname):
        shell_command = 'ls -1 ' + self._path + '/' + pathname
        return self._ssh_utils.command_in_ssh_command(shell_command)
