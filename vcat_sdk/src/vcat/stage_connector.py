class StageConnector(object):

    def __init__(self, cache, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._cache = cache
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._is_persisted = False
        self._cache_name = None

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

    def add_tree_names(self, stages_dict, filler_builder, **filler_kwargs):
        from vcat.rose_tree_traversable import traverse

        def add_tree_names_action(parent_ids, this_connector):
            filler = filler_builder(
                *this_connector.args(), **this_connector.kwargs())
            args, kwargs = filler.fill(**filler_kwargs)
            this_stage = {"function_name": this_connector.function_name(
            ), "args": args, "kwargs": kwargs, "parents": parent_ids}
            stages_dict[this_connector.name()] = this_stage
            return this_connector.name()

        return traverse(add_tree_names_action, self)

    def cache(self, name):
        self._cache_name = name

    def stage(self, next_stage):
        return StageConnector(self._cache, next_stage, [self])

    def run(self, filler_builder, **filler_kwargs):
        from vcat.rose_tree_traversable import lazy_traverse, force_results

        def run_action(previous_results, self):
            if self._has_run:
                return self._result

            upstream_result = None
            cache_name = self._cache_name
            if cache_name is None:
                upstream_result = force_results(previous_results)
                cache_name = self._auto_cache_name(upstream_result, filler_builder, **filler_kwargs)

            cached_result = self._cache.get(cache_name)
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
            self._cache.set(cache_name, self._result)
            return self._result

        return lazy_traverse(run_action, self)

    def _auto_cache_name(self, result, filler_builder, **filler_kwargs):
        from vcat.argument_hasher import ArgumentHasher
        from vcat.utils import merged_uuids

        new_args, new_kwargs = self.current_stage.fill_args_and_kwargs(filler_builder, **filler_kwargs)
        hasher = ArgumentHasher(new_args, new_kwargs)
        argument_hash = hasher.make_hash()

        upstream_hash = self._result_hash(result)

        return merged_uuids([argument_hash, upstream_hash, self.uuid()])

    def _result_hash(self, result):
        from vcat.utils import make_uuid

        return make_uuid(result)
