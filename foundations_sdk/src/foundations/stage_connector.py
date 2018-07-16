"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageConnector(object):

    def __init__(self, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._upstream_results = None

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

    def previous_nodes(self):
        return self._previous_connectors

    def _reset_state(self):
        from foundations.rose_tree_traversable import traverse

        def reset_action(parent_results, this_connector):
            this_connector._has_run = False
            this_connector._result = None

        traverse(reset_action, self)

    def add_tree_names(self, stage_hierarchy, filler_builder, **filler_kwargs):
        from foundations.rose_tree_traversable import traverse

        def add_tree_names_action(parent_ids, this_connector):
            filler = filler_builder(
                *this_connector.args(), **this_connector.kwargs())
            args, kwargs = filler.fill(**filler_kwargs)
            stage_hierarchy.entries[this_connector.uuid()].stage_args = args
            stage_hierarchy.entries[
                this_connector.uuid()].stage_kwargs = kwargs

        traverse(add_tree_names_action, self)

    def stage(self, next_stage):
        return StageConnector(next_stage, [self])

    def run(self, filler_builder, **filler_kwargs):
        from foundations.rose_tree_traversable import lazy_traverse

        return lazy_traverse(StageConnector._run_action(filler_builder, filler_kwargs), self)

    @staticmethod
    def _run_action(filler_builder, filler_kwargs):
        from foundations.rose_tree_traversable import force_results

        def run_action(previous_results, self):
            def fetch_upstream_result():
                if self._upstream_results is None:
                    self._upstream_results = force_results(previous_results)
                return self._upstream_results

            return self.current_stage.run(fetch_upstream_result, filler_builder, **filler_kwargs)

        return run_action