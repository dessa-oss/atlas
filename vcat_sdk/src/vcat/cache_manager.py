class CacheManager(object):

    def __init__(self):
        self._cache = None

    def cache(self):
        if self._cache is None:
            self._load()
        return self._cache

    def _load(self):
        from vcat.global_state import config_manager
        from vcat.null_cache import NullCache

        config = config_manager.config()

        if 'cache_implementation' in config:
            cache_implementation = config[
                'cache_implementation']
            cache_klass = cache_implementation['cache_type']
            cache_args = cache_implementation.get('constructor_arguments', [])
            self._cache = cache_klass(*cache_args)
        else:
            self._cache = NullCache()
