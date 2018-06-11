"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.utils import file_archive_name
from vcat.utils import file_archive_name_with_additional_prefix
from vcat.simple_tempfile import SimpleTempfile


class LocalBundledPipelineArchive(object):

    def __init__(self, archive_path, open_for_reading=False):
        import tarfile

        if open_for_reading:
            self._tar = tarfile.open(archive_path, "r:gz")
        else:
            self._tar = tarfile.open(archive_path, "w:gz")

    def __enter__(self):
        self._tar.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self._tar.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item, prefix=None):
        import dill as pickle

        with SimpleTempfile('w+b') as tempfile:
            pickle.dump(item, tempfile.file, protocol=2)
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
        import dill as pickle

        arcname = file_archive_name(prefix, name)

        for tar_info in self._tar:
            if tar_info.name == arcname:
                input_file = self._tar.extractfile(tar_info)
                try:
                    return pickle.load(input_file)
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
                return

    def _add_to_tar(self, tempfile, prefix, name):
        tempfile.file.flush()
        arcname = file_archive_name(prefix, name)
        self._tar.add(tempfile.path, arcname=arcname)
