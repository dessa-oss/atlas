class CacheManager(object):

    def __init__(self):
        self.cache = None

    def load(self):
        from vcat.global_state import config_manager
        from vcat.null_cache import NullCache

        if 'cache_implementation' in config_manager.config:
            cache_implementation = config_manager.config[
                'cache_implementation']
            cache_klass = cache_implementation['cache_type']
            cache_args = cache_implementation['constructor_arguments']
            self.cache = cache_klass(*cache_args)
        else:
            self.cache = NullCache()
