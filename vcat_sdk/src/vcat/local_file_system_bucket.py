class LocalFileSystemBucket(object):

    def __init__(self, path):
        from os.path import abspath
        from os import getcwd

        self._path = abspath(path or getcwd())

    def upload_from_string(self, name, data):
        self._log().debug('Uploading %s from string', name)

        self._ensure_path_exists(name)
        with open(self._full_path(name), 'w+b') as file:
            file.write(data)

    def upload_from_file(self, name, input_file):
        from shutil import copyfileobj

        self._log().debug('Uploading %s from %s', name, input_file.name)

        self._ensure_path_exists(name)
        with open(self._full_path(name), 'w+b') as file:
            copyfileobj(input_file, file)

    def exists(self, name):
        from os.path import isfile

        self._log().debug('Checking if %s exists', name)

        path = self._full_path(name)
        return isfile(path)

    def download_as_string(self, name):
        self._log().debug('Downloading %s', name)

        with open(self._full_path(name), 'rb') as file:
            return file.read()

    def download_to_file(self, name, output_file):
        from shutil import copyfileobj

        self._log().debug('Downloading %s to %s', name, output_file.name)

        with open(self._full_path(name), 'rb') as file:
            copyfileobj(file, output_file)

    def list_files(self, pathname):
        from glob import glob
        from os import getcwd

        self._log().debug('Getting listing with pathname %s', pathname)

        full_pathname = self._full_path(pathname)
        self._log().debug('Listing with expanded pathname is %s', full_pathname)
        full_paths = glob(full_pathname)
        return [self._remove_bucket_path_from_file(path) for path in full_paths]

    def _remove_bucket_path_from_file(self, path):
        return path[len(self._path)+1:]

    def _full_path(self, name):
        from os.path import join
        return join(self._path + '/' + name)

    def _ensure_path_exists(self, name):
        from distutils.dir_util import mkpath
        from os.path import isdir

        directory = self._directory_path(name)
        if not isdir(directory):
            mkpath(directory)

    def _directory_path(self, name):
        from os.path import dirname
        from os.path import join

        return join(self._path + '/' + dirname(name))

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
