class StageConnector(object):

    def __init__(self, cache, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._cache = cache
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._is_persisted = False
        self._cache_name = self._make_cache_name()

    def _make_cache_name(self):
        from uuid import uuid4
        return str(uuid4())

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
            filler = filler_builder(*this_connector.args(), **this_connector.kwargs())
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
        
        def run_action(previous_results, this_connector):
            if this_connector._has_run:
                return this_connector._result

            cached_result = this_connector._cache.get(this_connector._cache_name)
            # TODO: SUPPORT `MISSING` VS `None`
            if cached_result is not None:
                this_connector._has_run = True
                this_connector._result = cached_result
                return cached_result

            this_connector._result = this_connector.current_stage.run(
                force_results(previous_results), filler_builder, **filler_kwargs)
            this_connector._has_run = True
            this_connector._cache.set(this_connector._cache_name, this_connector._result)
            return this_connector._result

        return lazy_traverse(run_action, self)
