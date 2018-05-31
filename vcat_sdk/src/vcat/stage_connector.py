class StageConnector(object):

    def __init__(self, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._is_persisted = False
        self._cache_name = None
        self._allow_caching = True

    def uuid(self):
        return self.current_stage.uuid()

    def name(self):
        return self.current_stage.name()

    def function_name(self):
        return self.current_stage.function_name()

    def args(self):
        return self.current_stage.args

    def kwargs(self):
        return self.current_stage.kwargs

    def persist(self):
        self._is_persisted = True

    def previous_nodes(self):
        return self._previous_connectors

    def _reset_state(self):
        from vcat.rose_tree_traversable import traverse

        def reset_action(parent_results, this_connector):
            this_connector._has_run = False
            this_connector._result = None

        traverse(reset_action, self)

    def add_tree_names(self, stage_hierarchy, filler_builder, **filler_kwargs):
        from vcat.rose_tree_traversable import traverse

        def add_tree_names_action(parent_ids, this_connector):
            filler = filler_builder(
                *this_connector.args(), **this_connector.kwargs())
            args, kwargs = filler.fill(**filler_kwargs)
            stage_hierarchy.entries[this_connector.uuid()].stage_args = args
            stage_hierarchy.entries[
                this_connector.uuid()].stage_kwargs = kwargs

        traverse(add_tree_names_action, self)

    def set_global_cache_name(self, name):
        self._cache_name = name

    def disable_caching(self):
        self._allow_caching = False

    def stage(self, next_stage):
        return StageConnector(next_stage, [self])

    def run(self, filler_builder, **filler_kwargs):
        from vcat.rose_tree_traversable import lazy_traverse, force_results

        def run_action(previous_results, self):
            if self._has_run:
                return self._result

            upstream_result = None
            if self._allow_caching:
                cache_name = self._cache_name
                if cache_name is None:
                    upstream_result = force_results(previous_results)
                    cache_name = self._auto_cache_name(
                        upstream_result, filler_builder, **filler_kwargs)

                cached_result = self._fetch_cache(cache_name)
                # TODO: SUPPORT `MISSING` VS `None`
                if cached_result is not None:
                    self._has_run = True
                    self._result = cached_result
                    return cached_result

            if upstream_result is None:
                upstream_result = force_results(previous_results)

            self._result = self.current_stage.run(
                upstream_result, filler_builder, **filler_kwargs)
            self._has_run = True

            if self._allow_caching:
                self._submit_cache(cache_name, self._result)

            return self._result

        return lazy_traverse(run_action, self)

    def _fetch_cache(self, cache_name):
        from vcat.global_state import cache_manager
        return cache_manager.cache.get(cache_name)

    def _submit_cache(self, cache_name, value):
        from vcat.global_state import cache_manager
        return cache_manager.cache.set(cache_name, value)

    def _auto_cache_name(self, result, filler_builder, **filler_kwargs):
        from vcat.argument_hasher import ArgumentHasher
        from vcat.utils import merged_uuids

        new_args, new_kwargs = self.current_stage.fill_args_and_kwargs(
            filler_builder, **filler_kwargs)
        hasher = ArgumentHasher(new_args, new_kwargs)
        argument_hash = hasher.make_hash()

        upstream_hash = self._result_hash(result)

        return merged_uuids([argument_hash, upstream_hash, self.uuid()])

    def _result_hash(self, result):
        from vcat.utils import make_uuid

        return make_uuid(result, self._result_hash)
