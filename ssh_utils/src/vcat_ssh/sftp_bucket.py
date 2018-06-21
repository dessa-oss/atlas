class SFTPBucket(object):

    def __init__(self, path):
        from pysftp import Connection
        from vcat.global_state import config_manager

        self._connection = Connection(
            config_manager['remote_host'],
            config_manager['remote_user'],
            private_key=config_manager['key_path']
        )
        self._path = path

    def upload_from_string(self, name, data):
        from vcat.simple_tempfile import SimpleTempfile

        with SimpleTempfile('w+b') as temp_file:
            temp_file.write_and_flush(data)
            self.upload_from_file(name, temp_file)

    def upload_from_file(self, name, input_file):
        self._ensure_path_exists(name)
        with self.change_directory(name):
            self._connection.put(input_file.name)

    def exists(self, name):
        from os.path import basename

        with self.change_directory(name):
            return self._connection.exists(basename(name))

    def download_as_string(self, name):
        from vcat.simple_tempfile import SimpleTempfile
        from vcat.utils import byte_string

        with SimpleTempfile('w+b') as temp_file:
            self.download_to_file(name, temp_file)
            data_bytes = temp_file.read()
            return byte_string(data_bytes)

    def download_to_file(self, name, output_file):
        from os.path import basename

        with self.change_directory(name):
            self._connection.get(basename(name), output_file.name)

    def list_files(self, pathname):
        from fnmatch import fnmatch

        with self.change_directory(self._path):
            paths = self._connection.listdir()
            return filter(lambda path: fnmatch(path, pathname), paths)

    def _ensure_path_exists(self, name):
        self._connection.makedirs(self._directory_path(name))

    def change_directory(self, name):
        return self._connection.cd(self._directory_path(name))

    def _directory_path(self, name):
        from os.path import dirname
        from os.path import join

        return join(self._path, dirname(name))
