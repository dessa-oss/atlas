"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.utils import file_archive_name
from foundations.utils import file_archive_name_with_additional_prefix
from foundations_contrib.simple_tempfile import SimpleTempfile


class LocalBundledPipelineArchive(object):

    def __init__(self, archive_path, open_for_reading=False):
        self._archive_path = archive_path
        self._open_for_reading = open_for_reading
        self._tar = None

    def __enter__(self):
        self._open_archive()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._log().debug('Closing %s', self._archive_path)
        self._tar.close()
        self._tar = None

    def remove_archive(self):
        from os import remove
        remove(self._archive_path)

    def append(self, name, item, prefix=None):
        from foundations_internal.serializer import serialize_to_file

        with SimpleTempfile('w+b') as tempfile:
            serialize_to_file(item, tempfile.file)
            self._add_to_tar(tempfile, prefix, name + '.pkl')

    def append_binary(self, name, serialized_item, prefix=None):
        with SimpleTempfile('w+b') as tempfile:
            tempfile.file.write(serialized_item)
            self._add_to_tar(tempfile, prefix, name)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        self._tar.add(file_path, arcname=arcname)

    def fetch(self, name, prefix=None):
        from foundations_internal.serializer import deserialize_from_file

        arcname = file_archive_name(prefix, name)

        for tar_info in self._tar:
            if tar_info.name == arcname:
                input_file = self._tar.extractfile(tar_info)
                try:
                    return deserialize_from_file(input_file)
                finally:
                    input_file.close()

    def fetch_binary(self, name, prefix=None):
        arcname = file_archive_name(prefix, name)

        for tar_info in self._tar:
            if tar_info.name == arcname:
                input_file = self._tar.extractfile(tar_info)
                try:
                    return input_file.read()
                finally:
                    input_file.close()

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        from shutil import copyfileobj

        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)

        for tar_info in self._tar:
            if tar_info.name == arcname:
                input_file = self._tar.extractfile(tar_info)
                try:
                    with open(file_path, 'w+b') as file:
                        copyfileobj(input_file, file)
                finally:
                    input_file.close()
                return True
        return False

    def _add_to_tar(self, tempfile, prefix, name):
        tempfile.file.flush()
        arcname = file_archive_name(prefix, name)
        self._tar.add(tempfile.path, arcname=arcname)

    def _open_archive(self):
        import tarfile

        open_mode = 'r:gz' if self._open_for_reading else 'w:gz'
        self._log().debug('Opening %s with `%s` open mode', self._archive_path, open_mode)
        self._tar = tarfile.open(self._archive_path, open_mode)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
