class NullArchive(object):

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        pass

    def append_binary(self, name, serialized_item, prefix=None):
        pass

    def append_file(self, file_prefix, file_path, prefix=None):
        pass

    def fetch(self, name, prefix=None):
        return None

    def fetch_binary(self, name, prefix=None):
        return None

    def fetch_to_file(self, file_prefix, file_path, prefix=None):
        pass
