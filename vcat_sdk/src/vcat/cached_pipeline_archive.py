class CachedPipelineArchive(object):

    def __init__(self, archive_type, *constructor_args, **constructor_kwargs):
        self._archive = archive_type(*constructor_args, **constructor_kwargs)

    def __enter__(self):
        self._archive.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._archive.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item, prefix=None):
        key = self._cache_name(None, None, prefix, name, None)
        self._set_cache(key, item)
        return self._archive.append(name, item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        key = self._cache_name(None, None, prefix, name, None)
        self._set_cache_binary(key, serialized_item)
        return self._archive.append_binary(name, serialized_item, prefix)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        key = self._cache_name(file_prefix, file_path,
                               prefix, None, target_name)
        with open(file_path, 'rb') as file:
            self._set_cache_binary(key, file.read())
        return self._archive.append_file(file_prefix, file_path, prefix, target_name)

    def fetch(self, name, prefix=None):
        def fallback():
            return self._archive.fetch(name, prefix)

        key = self._cache_name(None, None, prefix, name, None)
        return self._cache().get_or_set_callback(key, fallback)

    def fetch_binary(self, name, prefix=None):
        def fallback():
            return self._archive.fetch_binary(name, prefix)

        key = self._cache_name(None, None, prefix, name, None)
        return self._cache().get_or_set_binary_callback(key, fallback)

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        def write_from_cache(result):
            with open(file_path, 'w+b') as file:
                file.write(result)

        def fallback():
            if self._archive.fetch_to_file(file_prefix, file_path, prefix, target_name):
                with open(file_path, 'rb') as file:
                    data = file.read()
                    self._set_cache(key, data)
                    return data
            else:
                self._set_cache(key, None)
                return None

        key = self._cache_name(file_prefix, file_path,
                               prefix, None, target_name)
        self._cache().get_binary_option(key).map(write_from_cache).fallback(fallback)
        return True

    def _cache(self):
        from vcat.global_state import cache_manager
        return cache_manager.cache()

    def _set_cache(self, key, value):
        self._cache().set(key, value)

    def _set_cache_binary(self, key, serialized_value):
        self._cache().set_binary(key, serialized_value)

    def _cache_name(self, file_prefix, file_path, prefix, name, target_name):
        from vcat.utils import merged_uuids

        key_parts = (file_prefix, file_path, prefix, name, target_name)
        string_key_parts = [str(part) for part in key_parts]
        return merged_uuids(string_key_parts)
