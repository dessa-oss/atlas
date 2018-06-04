from vcat.utils import file_archive_name
from vcat.utils import file_archive_name_with_additional_prefix


class LocalPipelineArchive(object):

    class Tempfile(object):

        def __init__(self, mode):
            self.path = None
            self.file = None
            self._mode = mode

        def __enter__(self):
            import tempfile
            import os

            file_descriptor, self.path = tempfile.mkstemp()
            self.file = os.fdopen(file_descriptor, self._mode)
            self.file.__enter__()

            return self

        def __exit__(self, exception_type, exception_value, traceback):
            import os

            try:
                self.file.__exit__()
            finally:
                os.remove(self.path)

    def __init__(self, open_for_reading=False):
        import tarfile
        if open_for_reading:
            self._tar = tarfile.open(self.archive(), "r:gz")
        else:
            self._tar = tarfile.open(self.archive(), "w:gz")

    def __enter__(self):
        self._tar.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self._tar.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item, prefix=None):
        import dill as pickle

        with self.Tempfile('w+b') as tempfile:
            pickle.dump(item, tempfile.file)
            self._add_to_tar(tempfile, prefix, name + '.pkl')

    def append_binary(self, name, serialized_item, prefix=None):
        with self.Tempfile('w+b') as tempfile:
            tempfile.file.write(serialized_item)
            self._add_to_tar(tempfile, prefix, name)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        self._tar.add(file_path, arcname=arcname)

    def fetch(self, name, prefix=None):
        raise NotImplementedError()

    def fetch_binary(self, name, prefix=None):
        raise NotImplementedError()

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        raise NotImplementedError()

    def archive_name(self):
        raise NotImplementedError()

    def archive(self):
        return self.archive_name()

    def _add_to_tar(self, tempfile, prefix, name):
        tempfile.file.flush()
        arcname = file_archive_name(prefix, name)
        self._tar.add(tempfile.path, arcname=arcname)
