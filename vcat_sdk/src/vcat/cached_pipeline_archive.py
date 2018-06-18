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
        key = self._cache_name(None, None, prefix, name, None)
        result = self._get_cache(key)
        if result is not None:
            return result

        result = self._archive.fetch(name, prefix)
        if result is not None:
            self._set_cache(key, result)

        return result

    def fetch_binary(self, name, prefix=None):
        key = self._cache_name(None, None, prefix, name, None)
        result = self._get_cache_binary(key)
        if result is not None:
            return result

        result = self._archive.fetch_binary(name, prefix)

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        key = self._cache_name(file_prefix, file_path,
                               prefix, None, target_name)
        result = self._get_cache_binary(key)
        if result is not None:
            with open(file_path, 'w+b') as file:
                file.write(result)

        if self._archive.fetch_to_file(file_prefix, file_path, prefix, target_name):
            with open(file_path, 'rb') as file:
                self._set_cache(key, file.read(result))
            return True

        return False

    def _set_cache(self, key, value):
        from vcat.global_state import cache_manager
        cache_manager.cache().set(key, value)

    def _set_cache_binary(self, key, serialized_value):
        from vcat.global_state import cache_manager
        cache_manager.cache().set_binary(key, serialized_value)

    def _get_cache(self, key):
        from vcat.global_state import cache_manager
        return cache_manager.cache().get(key)

    def _get_cache_binary(self, key):
        from vcat.global_state import cache_manager
        return cache_manager.cache().get_binary(key)

    def _cache_name(self, file_prefix, file_path, prefix, name, target_name):
        pass
