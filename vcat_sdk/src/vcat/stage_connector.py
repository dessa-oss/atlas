from vcat.stage_cache import StageCache


class StageConnector(object):

    def __init__(self, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._is_persisted = False
        self._cache_name = None
        self._allow_caching = True
        self._upstream_result = None

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
        from vcat.rose_tree_traversable import lazy_traverse

        return lazy_traverse(StageConnector._run_action(filler_builder, filler_kwargs), self)

    @staticmethod
    def _run_action(filler_builder, filler_kwargs):
        from vcat.rose_tree_traversable import force_results

        def run_action(previous_results, self):
            if self._has_run:
                return self._result

            def fetch_upstream_result():
                if self._upstream_result is None:
                    self._upstream_result = force_results(previous_results)
                return self._upstream_result

            stage_cache = StageCache(
                self._allow_caching,
                self._cache_name,
                self.current_stage,
                filler_builder,
                filler_kwargs,
                fetch_upstream_result
            )

            # TODO: SUPPORT `MISSING` VS `None`
            cached_result = stage_cache.fetch_cache()
            if cached_result is not None:
                self._has_run = True
                self._result = cached_result
                return cached_result

            if self._upstream_result is None:
                self._upstream_result = force_results(previous_results)

            self._result = self.current_stage.run(
                self._upstream_result, filler_builder, **filler_kwargs)
            self._has_run = True

            if self._allow_caching:
                stage_cache.submit_cache(self._result)

            return self._result

        return run_action