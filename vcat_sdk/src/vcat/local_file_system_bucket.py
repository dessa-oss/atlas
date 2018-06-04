class LocalFileSystemBucket(object):

    def __init__(self, path):
        from logging import getLogger
        self._log = getLogger(__name__)
        self._path = path

    def upload_from_string(self, name, data):
        self._log.debug('Uploading %s from string', name)

        self._ensure_path_exists(name)
        with open(self._full_path(name), 'w+b') as file:
            file.write(data)

    def upload_from_file(self, name, input_file):
        from shutil import copyfileobj

        self._log.debug('Uploading %s from %s', name, input_file.name)

        self._ensure_path_exists(name)
        with open(self._full_path(name), 'w+b') as file:
            copyfileobj(input_file, file)

    def exists(self, name):
        from os.path import isfile

        self._log.debug('Checking if %s exists', name)

        path = self._full_path(name)
        return isfile(path)

    def download_as_string(self, name):
        self._log.debug('Downloading %s', name)

        with open(self._full_path(name), 'rb') as file:
            return file.read()

    def download_to_file(self, name, output_file):
        from shutil import copyfileobj

        self._log.debug('Downloading %s to %s', name, output_file.name)

        with open(self._full_path(name), 'rb') as file:
            copyfileobj(file, output_file)

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
